""""""
from ..logger import log


def run_item_paths_tests(manager, item_id):
    """Run the path tests for the supplied item."""
    all_items = manager.get_data(all_items=True)
    item_path_errors = test_paths_link(item_id, all_items)
    if item_path_errors:
        message = "Error upgrading {}".format(item_id)
        log.test_result(message, item_path_errors)


def test_paths_link(item_id, all_items):
    """Test the paths (upgrades and components) for an item are consistent.

    Return a list of errors that were encountered."""
    all_items_data = all_items['data']
    errors = list()
    item_data = all_items_data[item_id]

    if 'into' in item_data:
        # Some items don't build into anything,
        # so we have to check.
        upgrades = item_data['into']
        for upgrade_id in upgrades:
            if upgrade_id not in all_items_data:
                # Upgrade doesn't exist.
                message = "{} lists {} as an upgrade, but it doesn't exist."
                errors.append(message.format(item_id, upgrade_id))
            else:
                upgrade = all_items_data[upgrade_id]
                if "from" not in upgrade or item_id not in upgrade['from']:
                    message = "{} upgrades to {}, but isn't listed as a component"
                    errors.append(message.format(item_id, upgrade_id))

    if 'from' in item_data:
        # There is something weird going on here. It doesn't see anything,
        # but there should be some items out of sync.
        components = item_data['from']

        for component_id in components:
            if component_id not in all_items_data:
                # Componenet doesn't exist
                message = "{} lists {} as an component, but it doesn't exist."
                errors.append(message.format(item_id, component_id))
            else:
                component = all_items_data[component_id]
                if "into" not in component or item_id not in component['into']:
                    message = "{} requires {}, but {} doesn't upgrade to {}"
                    errors.append(message.format(component_id, item_id, item_id, component_id))

    # Check items only rely on available components.
    if 'from' in item_data:
        components = item_data['from']
        for component_id in components:
            component = all_items_data[component_id]
            for map_id, item_is_available in item_data['maps'].items():
                if item_is_available and not component['maps'][map_id]:
                    message = "{} requires {}, but that item is not available on {}"
                    errors.append(message.format(item_id, component_id, map_id))

    return errors
