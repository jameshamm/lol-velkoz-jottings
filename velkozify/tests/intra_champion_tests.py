"""intra_champion_tests.py contains tests that check the internal consistency
of a champion's data.
"""
from ..data import DataManager


def run_intra_champion_tests(champion_name):
    """Run the tests for the supplied champion."""
    manager = DataManager()
    champion_data = manager.get_data(champion_name)
    print("Got data for {}".format(champion_name))
    print(champion_data.keys())
