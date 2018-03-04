from .downloader import ONLINE_LOCATIONS, download, get_latest_patch
from .storage import FILE_LOCATIONS, load

from urllib.error import URLError


def compress_name(champion_name):
    """To ensure champion names can be searched for and compared,
    the names need to be reduced.

    The process is to remove any characters not in the alphabet
    (apostrophe, space, etc) and then convert everything to lowercase.

    Note that reversing this is non-trivial, there are inconsistencies
    in the naming scheme used.

    Examples:
        Jhin -> jhin
        GALIO -> galio
        Aurelion Sol -> aurelionsol
        Dr. Mundo -> drmundo
        kha'zix -> khazix
    """
    compressed_name = "".join(c for c in champion_name if c.isalpha())
    return compressed_name.lower()


class DataNotFound(Exception):
    pass


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
            data = load(expected_file_location, data_format="json")
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
        ASSUMPTION: The champion name has been normalized to an expected name.
        This is not a great assumption as get_data is public.

        TODO: This function is messy to read, and uses strings everywhere.
        It should be reworked if possible when more data sets are added.
        TODO: Add caching to this function. If the data is downloaded from
        online, the data should be saved.
        """
        number_of_requested_data_sets = 0
        if champion_name is not None:
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
            return data

        # Find the data online
        try:
            data = self._download_data(query_type, query)
        except DataNotFound:
            message = "Could not find {} locally or online.".format(query)
            raise DataNotFound(message)
        else:
            return data

    def all_champion_names(self):
        """Return a dict with the known champion names.

        The format each entry follows is <compressed name>: <name>."""
        all_champions_data = self.get_data(all_champions=True)
        champion_names = all_champions_data["data"].keys()
        champion_names_dict = {
            compress_name(name): name for name in champion_names}
        return champion_names_dict
