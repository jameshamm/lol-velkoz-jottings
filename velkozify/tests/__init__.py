"""The registered test runners.

New test runners should be added here to make importing them easier.
"""
from .intra_champion_tests import run_intra_champion_tests
from .champion_recommended_items_test import run_champion_itemsets_tests
from .item_paths_test import run_item_paths_tests
from .intra_item_tests import run_intra_item_tests

__all__ = [
    # Champion test runners.
    "run_intra_champion_tests", "run_champion_itemsets_tests",

    # Item test runners.
    "run_intra_item_tests", "run_item_paths_tests"]
