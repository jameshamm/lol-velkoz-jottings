""""""

def run_item_paths_tests(manager):
    """"""
    all_items = manager.get_data(all_items=True)
    item_path_errors = test_paths_link(all_items)
    if item_path_errors:
        print("Upgrading items has {} issue(s)".format(
            len(item_path_errors)))
        print("\n".join((" " * 4) + error for error in item_path_errors))



def test_paths_link(all_items):
    """"""
    all_items_data = all_items['data']
    errors = list()

    for item_id, data in all_items_data.items():
        # import pdb; pdb.set_trace()
        if 'into' in data:
            # Some items don't build into anything,
            # so we have to check.
            upgrades = data['into']
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

        if 'from' in data:
            # There is something weird going on here. It doesn't see anything,
            # but there should be some items out of sync.
            components = data['from']

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
        
    return errors
