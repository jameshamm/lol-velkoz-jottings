"""intra_champion_tests.py contains tests that check the internal consistency
of a champion's data.
"""
from ..data import DataManager


def run_intra_champion_tests(champion_name):
    """Run the tests for the supplied champion."""
    manager = DataManager()
    champion_data = manager.get_data(champion_name)
    print("Running tests on {}".format(champion_name))

    spell_errors = test_champion_spells(champion_name, champion_data)
    if spell_errors:
        print("{} has spell {} issues".format(champion_name, len(spell_errors)))
        print("\n".join((" " * 4) + error for error in spell_errors))


def test_champion_spells(champion_name, champion_data):
    """Test that the spells a champion has have consistent data.
    
    Return a list of errors that were encountered."""
    spells_data = champion_data["data"][champion_name]["spells"]
    errors = list()

    # Test certain attributes are combined correctly and
    # are the correct length.
    # 'cost': [80, 90, 100, 110, 120] -> 'costBurn': '80/90/100/110/120'
    # 'range': [1075, 1075, 1075, 1075, 1075] -> 'rangeBurn': '1075'
    # 'maxrank': 5 -> len([80, 90, 100, 110, 120]) = 5
    attributes_to_test = ("cooldown", "cost", "range")
    for spell in spells_data:
        for attribute in attributes_to_test:
            values, string_values = spell[attribute], spell[attribute + "Burn"]
            # This is kinda hard to read. Move to a function?
            if not all(v == values[0] for v in values) and \
               "/".join(map(str, values)) != string_values:
                message = "Spell {}: {} does not match {}. "
                message += "{} is inconsistent with {}"

                errors.append(message.format(
                    spell["name"], attribute, attribute + "Burn",
                    values, string_values))

            if len(values) != spell["maxrank"]:
                message = "Spell {}: {} does not match {}. "
                message += "len({}) != {}"
                errors.append(message.format(
                    spell["name"], attribute, "maxrank",
                    values, spell["maxrank"]))

    return errors
