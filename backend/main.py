import json

import requests

from bs4 import BeautifulSoup
import logging
from flask import Flask, request, jsonify, Response, make_response

from flask_cors import CORS
import time

app = Flask(__name__, static_url_path="", static_folder="dist")
CORS(app)



plugin_name = "kubernetes"

FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger("Main")

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("bs4").setLevel(logging.WARNING)



jenkins_plugin_url = "https://updates.jenkins-ci.org/download/plugins/"

tag_value = "/icons/folder.gif"

alt_value = "[DIR]"


plugin_cache = []
cache_age = 0

@app.route("/", methods= ["GET"], strict_slashes=False)
def index():
    return app.send_static_file("index.html")


@app.route("/api/single", methods = ["GET", "POST"], strict_slashes=False)
def extract_plugin_info():
    data = request.args.get('plugin')

    logger.debug(f"Plugin request param: {data}")

    info = find_plugin(data)

    logger.debug(f"Returned data: {info}")

    return jsonify({"plugin": info, "total": len(plugin_cache), "found": 1})


@app.route("/api/multi", methods = ["GET", "POST"], strict_slashes=False)
def extract_plugin_info_list():

    logger.debug("Extracting json")
    logger.debug(f"Request is {dir(request)}")
    request_json = request.json
    if request_json is None:
        logger.warning("request.json returns None, looking up request.data instead")
        # Decode byte array and load into python dictionary
        request_json = json.loads(request.data.decode("utf-8"))

    logger.debug(f"Got request json: {request_json}")

    response_data = []

    for plugin in request_json["plugins"]:
        logger.info(f"Fetching data for plugin {plugin}")
        current = find_plugin(plugin)

        logger.info(f"Found data: {current}")
        if current:
            response_data.append(current)
    resp = jsonify({"plugins": response_data, "comment" : "data found for requets plugins", "purpose": 42, "total" : len(plugin_cache), "found": len(response_data), "looked_for": len(request_json["plugins"])})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


def find_version(url):

    href_keyword = "download"

    html = requests.get(url)

    soup = BeautifulSoup(html.content, "html.parser")

    rows = soup.find_all("tr")

    for row in rows:
        logger.debug("Found row in version page")
        anchor = row.find("a")
        # Return top element, as it is the ne
        if anchor and "href" in anchor.attrs and href_keyword in anchor.attrs["href"]:
            logger.info("Found version information, returning it")
            return anchor.text
    logger.warning("Did not find version info, returning None")
    return None


def find_plugin(plugin_name):
    current_time = time.time()

    logger.info("Current time: {}".format(current_time))

    global cache_age

    logger.info("Cache age: {}".format(cache_age))


    age_of_cache = current_time - cache_age

    logger.info("Cache age is {}".format(age_of_cache))
    logger.info("Cache length is: {}".format(len(plugin_cache)))

    if ":" in plugin_name:
        logger.debug(f"Stripping : from {plugin_name}")
        plugin_name = plugin_name[0:plugin_name.index(":")]
        logger.debug(f"Stripped name: {plugin_name}")

    if len(plugin_cache) > 0 and age_of_cache < 3600:
        logger.info("Cache is younger than 1 hour, fetching from cache")
        return find_plugin_in_cache(plugin_name)
    else:
        logger.info("Cache is older than 1  hour, fetching new cache")
        logger.info("Preparing plugin cache")
        fill_cache()
        cache_age = time.time()
        logger.info(f"{len(plugin_cache)} plugins cached")
        return find_plugin_in_cache(plugin_name)

def find_plugin_in_cache(plugin_name):
    for name in plugin_cache:
        if plugin_match(name, plugin_name):
            lower_name = name.lower().strip("/")
            logger.debug(f"Found: {lower_name}")
            full_url = jenkins_plugin_url + name
            logger.debug(f"Opening plugin page at: {full_url}")
            version_string = find_version(full_url)
            plugin_formatted = f"{lower_name}:{version_string}"
            logger.debug(f"Returning plugin formatted as: {plugin_formatted}")
            return plugin_formatted
    return None

def plugin_match(path, name):
    path_stripped = path.lower().strip("/")
    logger.debug(f"Checking if {name} == {path_stripped} excluding")
    if name and str(name) == path_stripped:
        logger.debug("Found match!")
        return True
    return False


def fill_cache():
    logging.info(f"Looking for plugins @ {jenkins_plugin_url}")

    html = requests.get(f"{jenkins_plugin_url}", timeout=300)

    soup = BeautifulSoup(html.content, 'html.parser')

    logger.info("Looking for table rows")

    logger.info("Resetting cache array")

    global plugin_cache

    plugin_cache = []

    rows = soup.find_all("tr")

    if rows and len(rows) > 0:
        logger.info(f"Found {len(rows)} rows")
    else:
        logger.error("Did not find any rows!!")

    for row in rows:
        img = row.find("img")
        if img and "alt" in img.attrs and img.attrs["alt"] and alt_value in img.attrs["alt"]:
            logger.debug("Found valid tag")
            anchor = row.find("a")
            name = anchor.text
            logger.debug(f"Checking plugin {name}")
            logger.debug(f"name: {plugin_name}")
            plugin_cache.append(anchor.text)
        else:
            logger.debug("failed to find alt tag. Skipping")
    logger.error(f"Did not find {plugin_name}")
    return None


def get_plugin_cache_length():
    global plugin_cache
    return len(plugin_cache)