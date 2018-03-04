import json
import os


LOCAL_STORAGE_FOLDER = ".data_sets"


def load(filename, data_format=None):
    """Load the contents of a file."""
    with open(filename, 'r') as file:
        if data_format is not None:
            # Coerce the data
            if data_format == "json":
                return json.loads(file)

            message = "Data format ({}) is not known".format(data_format)
            raise ValueError(message)

        return file.readlines()


def save(filename, contents, data_format=None):
    """Save the contents to the supplied location.

    If a format is specified, save with that format.
    """
    raise NotImplementedError("Saving is not ready yet.")


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