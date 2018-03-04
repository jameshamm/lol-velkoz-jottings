import json
import os


LOCAL_STORAGE_FOLDER = "data_sets"


def load(filename, data_format=None):
    """Load the contents of a file."""
    with open(filename, 'r') as file:
        if data_format is not None:
            # Coerce the data
            if data_format == "json":
                return json.load(file)

            message = "Data format ({}) is not known".format(data_format)
            raise ValueError(message)

        return file.readlines()


def save(filename, contents, data_format=None):
    """Save the contents to the supplied location.

    If a format is specified, save with that format.
    """
    # If the folder structure doesn't exist, make it.
    directory_name = os.path.dirname(filename)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    # Save the file with the proposed data format.
    with open(filename, 'w') as file:
        if data_format is not None:
            if data_format == "json":
                json.dump(contents, file)
                return

            message = "Data format ({}) is not known".format(data_format)
            raise ValueError(message)

        file.write(contents)


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


def expected_filename(query_type, query, patch, region):
    """Return the expected filename for a data set."""
    get_file_location = FILE_LOCATIONS[query_type]

    if query_type == "champion":
        # Unlike other query types, the champion name is needed.
        # It is presumed the champion name has already been normalized.
        return get_file_location(query, patch, region)

    return get_file_location(patch, region)
