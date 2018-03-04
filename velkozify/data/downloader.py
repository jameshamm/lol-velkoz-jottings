"""downloader.py contains all the necessary functions and classes to download
data sets from a riot endpoint."""
import json
import os

from time import sleep
from urllib import request
from urllib.error import URLError


LOCAL_STORAGE_FOLDER = ".data_sets"


class DataNotFound(Exception):
    pass


def normalize(champion_name):
    """To access a champion data set online,
    the name must be normalize to a specific format.

    Each word in the name must be in titlecase
        jhin -> Jhin
        GALIO -> Galio
    Spaces are removed
        Aurelion Sol -> AurelionSol
        xin zhao -> XinZhao
    Apostrophes are removed (but do not count as word separators)
        Cho'Gath -> Chogath (Notice the lowercase g)
        kha'ZIX -> Khazix
    """
    return champion_name.replace("'", "").title().replace(" ", "")


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
    """Return the known versions."""
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version_data = download(version_url, data_format="json")
    return version_data


def get_latest_patch():
    """Return the most recent patch."""
    version_data = get_version_data()

    # latest patch is the first in the version data list
    return version_data[0]


def _get_champion_saved_location(champion_name, patch, region):
    """Return the location a champion data set is expected to be.

    This function defines the expected (sub)folder format and
    needs to be updated if the format changes."""
    return os.path.join(
        LOCAL_STORAGE_FOLDER, patch, region,
        "champions", str(champion_name) + ".json")


def _get_all_champions_saved_location(patch, region):
    """Return the location the data set with all champions is expected to be.

    This function defines the expected (sub)folder format and
    needs to be updated if the format changes."""
    return os.path.join(LOCAL_STORAGE_FOLDER, patch, region, "champion.json")


def _get_all_items_saved_location(patch, region):
    """Return the location the data set with all champions is expected to be.

    This function defines the expected (sub)folder format and
    needs to be updated if the format changes."""
    return os.path.join(LOCAL_STORAGE_FOLDER, patch, region, "item.json")


FILE_LOCATIONS = {
    "champion": _get_champion_saved_location,
    "all_champions": _get_all_champions_saved_location,
    "all_items": _get_all_items_saved_location}


# NOTE: These use an insecure http connection.
ONLINE_LOCATIONS = {
    "champion": "http://ddragon.leagueoflegends.com/cdn/{}/data/{}/champion/{}.json",
    "all_champions": "http://ddragon.leagueoflegends.com/cdn/{}/data/{}/champion.json",
    "all_items": "http://ddragon.leagueoflegends.com/cdn/{}/data/{}/item.json"
}


class DataManager:
    """Provide data in a convenient form.

    This manager keeps track of details like the patch to retrieve data for.

    If the data is not available, an attempt will be made to download it.
    """
    def __init__(self, patch=None):
        self.patch = get_latest_patch() if patch is None else patch
        self.region = "en_US"

    def _get_saved_data(self, query_type, query):
        """Return data if it is saved locally.

        Otherwise raise a DataNotFound Error.
        """
        get_file_location = FILE_LOCATIONS[query_type]

        if query_type == "champion":
            # Unlike other query types, the champion name is needed.
            # It is presumed the champion name has already been normalized.
            expected_file_location = get_file_location(
                query, patch=self.patch, region=self.region)
        else:
            expected_file_location = get_file_location(
                patch=self.patch, region=self.region)

        try:
            with open(expected_file_location, 'r') as file:
                data = json.load(file)
        except IOError:
            message = "Could not locate {} at {}".format(
                query_type, expected_file_location)
            raise DataNotFound(message)
        else:
            return data

    def _download_data(self, query_type, query):
        """Return data if it is found online.

        Otherwise raise a DataNotFound Error.
        """
        url = ONLINE_LOCATIONS[query_type]

        if query_type == "champion":
            # It is presumed the champion name has already been normalized.
            url = url.format(self.patch, self.region, query)
        else:
            url = url.format(self.patch, self.region)

        try:
            data = download(url, data_format="json")
        except URLError:
            message = "Could not locate {} at {}".format(
                query_type, url)
            raise DataNotFound(message)
        else:
            return data

    def get_data(self, champion_name=None,
                 all_champions=None, all_items=None):
        """Get the data on a particular champion, all champions, or
        all items.

        Return the source of the data, followed by the data.
        If the data is not available anywhere, a DataNotFound Error
        will be raised.

        ASSUMPTION: The file format for every data set is presumed to be json.

        TODO: This function is messy to read, and uses strings everywhere.
        It should be reworked if possible when more data sets are added.
        """
        number_of_requested_data_sets = 0
        if champion_name is not None:
            champion_name = normalize(champion_name)
            query_type, query = "champion", champion_name
            number_of_requested_data_sets += 1

        if all_champions is not None:
            query_type, query = "all_champions", "all_champions"
            number_of_requested_data_sets += 1

        if all_items is not None:
            query_type, query = "all_items", "all_items"
            number_of_requested_data_sets += 1

        # Only one data set should be requested at once
        if number_of_requested_data_sets != 1:
            message = "More than one data set was requested at once."
            raise ValueError(message)

        # Look locally for the data
        try:
            data = self._get_saved_data(query_type, query)
        except DataNotFound:
            pass
        else:
            return "locally", data

        # Find the data online
        try:
            data = self._download_data(query_type, query)
        except DataNotFound:
            message = "Could not find {} locally or online.".format(query)
            raise DataNotFound(message)
        else:
            return "online", data
