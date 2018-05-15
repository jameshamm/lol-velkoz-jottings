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
    errors = []

    errors += check_upgrades_link_back(item_id, all_items_data)
    errors += check_components_link_forward(item_id, all_items_data)
    errors += check_all_components_are_available(item_id, all_items_data)

    return errors


def check_upgrades_link_back(item_id, all_items_data):
    """Every upgrade this item can build into should list this item
    as a component.

    Return a list with the errors encountered."""
    item_data = all_items_data[item_id]
    if 'into' not in item_data:
        return []

    errors = []
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

    return errors


def check_components_link_forward(item_id, all_items_data):
    """Every component should list this item as an upgrade.

    Return a list of errors encountered."""
    item_data = all_items_data[item_id]
    if 'from' not in item_data:
        return []

    errors = []
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
                errors.append(message.format(
                    component_id, item_id, item_id, component_id))

    return errors


def check_all_components_are_available(item_id, all_items_data):
    """Every component of this item should be available
    (but maybe not purchasable) on the same map as this.
    The converse does not hold, some upgrades may not be available on the
    same maps as all its components.

    Return a list of errors encountered."""
    item_data = all_items_data[item_id]
    if 'from' not in item_data:
        return []

    errors = []
    components = item_data['from']
    for component_id in components:
        component = all_items_data[component_id]
        for map_id, item_is_available in item_data['maps'].items():
            if item_is_available and not component['maps'][map_id]:
                message = "{} requires {}, which is not available on {}"
                errors.append(message.format(item_id, component_id, map_id))

    return errors
