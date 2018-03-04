"""downloader.py contains all the necessary functions and classes to download
data sets from a riot endpoint."""
import json

from time import sleep
from urllib import request


def download(url, data_format=None):
    """Download whatever is at the supplied url.

    There is rate limiting done by this function. This means function
    may be a bottleneck if a lot of data needs to be downloaded.

    If a data format is given, try and coerce the data into that format.
    Otherwise return the raw data.

    Currently json is the only data format currently implemented.
    """
    req = request.Request(url)
    data = request.urlopen(req).read()

    if data_format is not None:
        # Coerce the data
        if data_format == "json":
            data = json.loads(data)
        else:
            message = "Data format ({}) is not known".format(data_format)
            raise ValueError(message)

    sleep(0.5)  # Simulate rate limiting by sleeping for half a second.
    return data


def get_version_data():
    """Return the known patches/versions."""
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version_data = download(version_url, data_format="json")
    return version_data


def get_latest_patch():
    """Return the most recent patch."""
    version_data = get_version_data()

    # latest patch is the first in the version data list
    return version_data[0]


# NOTE: These use an insecure http connection.
WEBSITE_PREFIX = "http://ddragon.leagueoflegends.com/cdn/{}/data/{}/"

ONLINE_LOCATIONS = {
    "champion": WEBSITE_PREFIX + "champion/{}.json",
    "all_champions": WEBSITE_PREFIX + "champion.json",
    "all_items": WEBSITE_PREFIX + "item.json"
}
