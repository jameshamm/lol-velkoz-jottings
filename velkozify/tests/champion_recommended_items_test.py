"""champion_recommended_items_test.py contains tests that check the internal consistency
of a champion's data.

All test will be named in the format test_*
"""
from ..logger import log


def run_champion_itemsets_tests(manager, champion_name):
    """Run the tests for the supplied champion."""
    champion_data = manager.get_data(champion_name)
    all_items = manager.get_data(all_items=True)

    itemset_errors = test_champion_itemsets(champion_name, champion_data, all_items)
    if itemset_errors:
        message = "Error with the itemset for {}".format(champion_name)
        log.test_result(message, itemset_errors)


def test_champion_itemsets(champion_name, champion_data, all_items):
    """Test the item sets recommended for a champion are consistent.

    Return a list of errors that were encountered."""
    itemset_data = champion_data["data"][champion_name]["recommended"]
    all_items_data = all_items['data']
    errors = list()

    # Check the starting items are affordable.
    for recommended_items in itemset_data:
        mode = recommended_items['mode']
        if mode == "ARAM":
            starting_gold = 1400
        elif mode == "CLASSIC":
            _map = recommended_items['map']
            if _map == "SR":
                starting_gold = 500
            else:
                # TODO: gold by mode AND map
                continue
        else:
            # TODO: gold for other modes.
            continue

        total_cost = 0
        starting_items = recommended_items['blocks'][0]['items']
        for item in starting_items:
            _id, count = item['id'], item['count']
            item_data = all_items_data[_id]
            total_cost += item_data['gold']['base'] * count

        if total_cost > starting_gold:
            # The starting items cost too much.
            message = "Starting items on {} cost too much, {} > {}"
            errors.append(message.format(mode, total_cost, starting_gold))

    # TODO: Check the items are available on the mode they are recommended for.

    return errors
