import unittest
import json
from flask import Flask, Blueprint, redirect, views, abort as flask_abort
from flask.signals import got_request_exception, signals_available
from flask import json

from main import app




def test_single_plugin_valid():
    response = app.test_client().post("/api/single?plugin=kubernetes", content_type="application/json")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert "plugin" in data
    assert "kubernetes:" in data["plugin"]


def test_single_plugin_empty_input():
    response = app.test_client().post("/api/single", content_type="application/json")

    assert response.status_code == 500


def test_multi_plugins_valid():
    response = app.test_client().post("/api/multi",
                                      data=json.dumps({"plugins": ["kubernetes", "git", "testlink"]}),
                                      content_type="application/json")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert "plugins" in data
    assert type(data["plugins"]) == list
    assert len(data["plugins"]) == 3
    assert "comment" in data

def test_multi_plugins_invalid_plugins_in_list():
    response = app.test_client().post("/api/multi",
                                      data=json.dumps({"plugins": ["kubernetes", "git", "deadplugin", "fakeplugin", "jauda"]}),
                                      content_type="application/json")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert "plugins" in data
    assert type(data["plugins"]) == list
    assert len(data["plugins"]) == 2
    assert "comment" in data


def test_multi_plugins_empty_list():
    response = app.test_client().post("/api/multi",
                                      data=json.dumps({"plugins": []}),
                                      content_type="application/json")

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert "plugins" in data
    assert type(data["plugins"]) == list
    assert len(data["plugins"]) == 0
    assert "comment" in data