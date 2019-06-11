import requests

from bs4 import BeautifulSoup
import logging

plugin_name = "kubernetes"

FORMAT = "%(asctime)-15s - %(levelname)s:%(name)s:%(message)s"
logging.basicConfig(level=logging.INFO, format=FORMAT)

logger = logging.getLogger("Main")


jenkins_plugin_url = "https://updates.jenkins-ci.org/download/plugins/"

tag_value = "/icons/folder.gif"

alt_value = "[DIR]"


def find_version(url):

    href_keyword = "download"

    html = requests.get(url)

    soup = BeautifulSoup(html.content, "html.parser")

    rows = soup.find_all("tr")

    for row in rows:
        anchor = row.find("a")
        # Return top element, as it is the ne
        if anchor and "href" in anchor.attrs and href_keyword in anchor.attrs["href"]:
            return anchor.text
    return None


def find_plugin(plugin_name):
    html = requests.get(f"{jenkins_plugin_url}")

    soup = BeautifulSoup(html.content, 'html.parser')

    rows = soup.find_all("tr")

    logger.info(rows)

    for row in rows:
        img = row.find("img")
        if img and "alt" in img.attrs and img.attrs["alt"] and alt_value in img.attrs["alt"]:
            logger.debug("Found valid tag")
            anchor = row.find("a")
            name = anchor.text

            if name and plugin_name == name.lower().strip("/"):
                lower_name = name.lower().strip("/")
                logger.info(f"Found {lower_name}")
                full_url = jenkins_plugin_url + name
                version_string = find_version(full_url)
                return f"{lower_name}:{version_string}"
        else:
            logger.info("failed to find alt tag")
    return None

plugin = find_plugin(plugin_name)



logger.info(f"{plugin}")

logger.info("done")



