import json
import os


LOCAL_STORAGE_FOLDER = "data_sets"
FILE_LOCATION_ENDINGS = {
    "all_champions": "champion.json",
    "all_items": "item.json"}


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


def expected_filename(query_type, query, patch, region):
    """Return the expected filename for a data set."""

    file_location_prefix = os.path.join(LOCAL_STORAGE_FOLDER, patch, region)

    if query_type == "champion":
        # Unlike other query types, the champion name is needed.
        # It is presumed the champion name has already been normalized.
        return os.path.join(
            file_location_prefix, "champions", str(query) + ".json")

    return os.path.join(
        file_location_prefix, FILE_LOCATION_ENDINGS[query_type])
