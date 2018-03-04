"""downloader.py contains all the necessary functions and classes to download
data sets from a riot endpoint."""
import json
import os

from time import sleep
from urllib import request

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
            data = json.loads(data.decode('utf-8'))
        else:
            message = "Data format ({}) is not known".format(data_format)
            raise ValueError(message)

    sleep(0.5)  # Simulate rate limiting by sleeping for half a second.
    return data


def get_version_data():
    """Return the known versions."""
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    version_data = json.loads(download(version_url))
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


class DataManager:
    """Provide data in a convenient form.

    This manager keeps track of details like the patch to retrieve data for.

    If the data is not available, an attempt will be made to download it.
    """
    def __init__(self, patch=None):
        self.patch = get_latest_patch() if patch is None else patch
        self.region = "en_US"

    def _get_saved_data(self, champion_name=None,
                        all_champions=None, all_items=None):
        """Return data if it is saved locally.

        Only one data set should be requested at a time.

        TODO: The api for this could be improved.
        ASSUMPTION: The file format is presumed to be json.
        """
        # Check the query is for only one data set.
        if sum(q is not None for q in
               (champion_name, all_champions, all_items)) != 1:
            message = "More than one data set was requested at once."
            raise ValueError(message)

        if all_champions is not None:
            query = "all_champions"
            expected_file_location = _get_all_champions_saved_location(
                patch=self.patch, region=self.region)
        elif all_items is not None:
            query = "all_items"
            expected_file_location = _get_all_items_saved_location(
                patch=self.patch, region=self.region)
        else:
            query = champion_name
            expected_file_location = _get_champion_saved_location(
                champion_name, patch=self.patch, region=self.region)

        try:
            with open(expected_file_location, 'r') as file:
                data = json.load(file)
        except IOError:
            message = "Could not locate {} at {}".format(
                query, expected_file_location)
            raise DataNotFound(message)
        else:
            return data

    def get_data(self, champion_name=None,
                 all_champions=None, all_items=None):
        """Get the data on a particular champion.

        Return the source of the data, followed by the data."""
        champion_name = normalize(champion_name)

        # Look locally for the data
        try:
            data = self._get_saved_data(
                champion_name, all_champions, all_items)
        except DataNotFound:
            pass
        else:
            return "locally", data

        # Find the data online
        # NOTE: This uses an insecure http connection.
        url = "http://ddragon.leagueoflegends.com/cdn/{}/data/{}/champion/{}.json"
        url = url.format(self.patch, self.region, champion_name)
        raise NotImplementedError("Can't fetch data online yet.")
