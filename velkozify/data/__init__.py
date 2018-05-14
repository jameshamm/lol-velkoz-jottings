"""This module (data) is for making access to data sets as easy as possible.

Example usage to print out all the champion names in the current patch
>>> d = DataManager()
>>> champion_names = d.all_champion_names()
>>> print(champion_names.values())
"""
from .downloader import expected_url, download, get_latest_patch, get_version_data
from ..logger import log
from .storage import expected_filename, load, save

from urllib.error import URLError


class DataNotFound(Exception):
    """Thrown if data that was requested could not be found."""
    pass


class DataManager:
    """Provide data in a convenient form.

    This manager keeps track of details like the patch to retrieve data for.

    If the data is not available, an attempt will be made to download it.
    """
    def __init__(self, patch=None, region=None):
        """Example:
            DataManager()
            DataManager(patch="8.5.1")
            DataManager(patch="6.24.1", region="en_GB")
        """
        if patch is None:
            self.patch = get_latest_patch()
        else:
            # Verify the patch supplied is known.
            known_patches = get_version_data()
            if patch in known_patches:
                self.patch = patch
            else:
                raise ValueError(f"Patch '{patch}' is not known or available.")

        self.region = "en_US" if region is None else region
        log.info(f"Using patch '{self.patch}'' and region '{self.region}'")

    def _get_saved_data(self, query_type, query):
        """Return data if it is saved locally.

        Otherwise raise a DataNotFound Error.
        """
        filename = expected_filename(
            query_type, query, patch=self.patch, region=self.region)

        try:
            data = load(filename, data_format="json")
        except IOError:
            message = "Could not locate {} at {}".format(
                query_type, filename)
            raise DataNotFound(message)
        else:
            return data

    def _download_data(self, query_type, query):
        """Return data if it is found online.

        Otherwise raise a DataNotFound Error.
        """
        url = expected_url(
            query_type, query, patch=self.patch, region=self.region)

        try:
            data = download(url, data_format="json")
        except URLError:
            message = "Could not locate {} at {}".format(
                query_type, url)
            raise DataNotFound(message)
        else:
            return data

    def get_data(self, champion_name=None,
                 all_champions=None, all_items=None, force_download=False):
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
        # This is messy, but has nicer documentation than **kwargs.
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
            message = "Expected one data set to be requested, got {}"
            raise ValueError(message.format(number_of_requested_data_sets))

        if not force_download:
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
            # Save the data so that it doesn't need to be downloaded again.
            filename = expected_filename(
                query_type, query, patch=self.patch, region=self.region)

            try:
                save(filename, data, data_format="json")
            except IOError:
                pass
            else:
                log.info(f"Saved the data set for {query} to {filename}")

            return data

    def all_champion_names(self):
        """Return a dict with the known champion names.

        The format each entry follows is <compressed name>: <name>."""
        all_champions_data = self.get_data(all_champions=True)
        champion_names = all_champions_data["data"].keys()
        champion_names_dict = {
            compress_name(name): name for name in champion_names}
        return champion_names_dict


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
