"""downloader.py contains all the necessary functions and classes to download
data sets from a riot endpoint."""
import json
import sys

from ..logger import log

from time import sleep
from urllib import request


LATEST_PATCH = None
VERBOSE = True  # Messy method to find out what online requests are being made.


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
            # json.loads works on bytes for python>=3.6
            # and just strings for previous versions.
            # This check is to support previous python versions
            # and probably needs a work around instead.
            version_info = sys.version_info
            if version_info.major == 3 and version_info.minor <= 5:
                # Convert the bytes to a string
                data = data.decode()
            data = json.loads(data)
        else:
            message = "Data format ({}) is not known".format(data_format)
            raise ValueError(message)

    if VERBOSE:
        log.log(url, name="REQUEST")

    sleep(0.5)  # Simulate rate limiting by sleeping for half a second.
    return data


def get_version_data():
    """Return the known patches/versions."""
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version_data = download(version_url, data_format="json")
    return version_data


def get_latest_patch():
    """Return the most recent patch."""
    global LATEST_PATCH
    if LATEST_PATCH is None:
        version_data = get_version_data()
        # latest patch is the first in the version data list
        LATEST_PATCH = version_data[0]
    return LATEST_PATCH


# Fill this in with the patch, then the region
# For example: http://ddragon.leagueoflegends.com/cdn/8.5.1/data/en_US/
# NOTE: These use an insecure http connection.
WEBSITE_PREFIX = "http://ddragon.leagueoflegends.com/cdn/{}/data/{}/"

ONLINE_LOCATIONS = {
    "champion": WEBSITE_PREFIX + "champion/{}.json",
    "all_champions": WEBSITE_PREFIX + "champion.json",
    "all_items": WEBSITE_PREFIX + "item.json"
}


def expected_url(query_type, query, patch, region):
    """Return the expected url the data set will be available from."""
    url = ONLINE_LOCATIONS[query_type]

    if query_type == "champion":
        # It is presumed the champion name has already been normalized.
        return url.format(patch, region, query)

    return url.format(patch, region)
