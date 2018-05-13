""""""


def run_intra_item_tests(manager, item_id):
    """Run the tests for the supplied champion."""
    all_items = manager.get_data(all_items=True)

    item_errors = test_item(item_id, all_items)
    if item_errors:
        print("{} has spell {} issue(s)".format(
            item_id, len(item_errors)))
        print("\n".join((" " * 4) + error for error in item_errors))


def test_item(item_id, all_items):
    """"""
    all_items_data = all_items['data']
    errors = list()

    # Check an item doesn't sell for more than it costs.
    prices = all_items_data[item_id]['gold']
    if prices['sell'] > prices['total']:
        message = "{} can be sold for more than it costs, {} > {}"
        errors.append(message.format(item_id, prices['sell'], prices['total']))

    return errors
