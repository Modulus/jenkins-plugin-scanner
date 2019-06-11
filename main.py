import requests

from bs4 import BeautifulSoup
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)



plugin_name = "kubernetes"

FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger("Main")

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("bs4").setLevel(logging.WARNING)



jenkins_plugin_url = "https://updates.jenkins-ci.org/download/plugins/"

tag_value = "/icons/folder.gif"

alt_value = "[DIR]"


@app.route("/", methods = ["GET", "POST"])
def extract_plugin_info():

    data = request.args.get('plugins')

    logger.info(f"Plugin request param: {data}")

    info = find_plugin(data)

    logger.info(f"Returned data: {info}")

    return jsonify({"plugin": info})


@app.route("/multi", methods = ["GET", "POST"])
def extract_plugin_info_list():

    logger.info("Extracting json")

    request_json = request.json

    logger.info(f"Got request json: {request_json}")

    response_data = []

    for plugin in request_json["plugins"]:
        logger.info(f"Fetching data for plugin {plugin}")
        current = find_plugin(plugin)

        logger.info(f"Found data: {current}")
        if current:
            response_data.append(current)

    return jsonify({"data": response_data, "comment" : "data found for requets plugins", "purpose": 42})



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

    if ":" in plugin_name:
        logger.info(f"Stripping : from {plugin_name}")
        plugin_name = plugin_name[0:plugin_name.index(":")]
        logger.info(f"Stripped name: {plugin_name}")

    logging.info(f"Looking for plugins @ {jenkins_plugin_url}")

    html = requests.get(f"{jenkins_plugin_url}")

    soup = BeautifulSoup(html.content, 'html.parser')

    logger.info("Looking for table rows")

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
            if plugin_match(name, plugin_name):
                lower_name = name.lower().strip("/")
                logger.info(f"Found: {lower_name}")
                full_url = jenkins_plugin_url + name
                logger.info(f"Opening plugin page at: {full_url}")
                version_string = find_version(full_url)
                plugin_formatted = f"{lower_name}:{version_string}"
                logger.info(f"Returning plugin formatted as: {plugin_formatted}")
                return plugin_formatted
        else:
            logger.debug("failed to find alt tag. Skipping")
    logger.error(f"Did not find {plugin_name}")
    return None

def plugin_match(path, name):
    path_stripped = path.lower().strip("/")
    logger.info(f"Checking if {name} == {path_stripped} excluding")
    if name and str(name) == path_stripped:
        logger.info("Found match!")
        return True
    return False


#plugin = find_plugin(plugin_name)
#
# logger.info(f"{plugin}")
#
# logger.info("done")



