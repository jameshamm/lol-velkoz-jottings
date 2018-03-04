from ..data.downloader import DataManager


def run_intra_champion_tests(champion_name):
    """Run the tests for the supplied champion."""
    manager = DataManager()
    _, champion_data = manager.get_data(champion_name)
    print("Got data for {}".format(champion_name))
    print(champion_data.keys())
