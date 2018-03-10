"""intra_champion_tests.py contains tests that check the internal consistency
of a champion's data.
"""
from ..data import DataManager


def run_intra_champion_tests(champion_name):
    """Run the tests for the supplied champion."""
    manager = DataManager()
    champion_data = manager.get_data(champion_name)

    spell_errors = test_champion_spells(champion_name, champion_data)
    if spell_errors:
        print("{} has spell {} issues".format(
            champion_name, len(spell_errors)))
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
                message = "Spell {}: {} does not match maxrank. "
                message += "len({}) != {}"
                errors.append(message.format(
                    spell["name"], attribute, values, spell["maxrank"]))

        # Check the effects all join together correctly.
        effects, string_effects = spell["effect"], spell["effectBurn"]
        if len(effects) != len(string_effects):
            message = "Spell {}: effect does not match effectBurn. "
            message += "len({}) != len({})"
            errors.append(message.format(
                spell["name"], effects, string_effects))

        for effect, string_effect in zip(effects, string_effects):
            # Skip any null entries.
            if effect is None and string_effect is None:
                continue

            if len(effect) != spell["maxrank"]:
                message = "Spell {}: effect does not match maxrank. "
                message += "len({}) != {}"
                errors.append(message.format(
                    spell["name"], effect, spell["maxrank"]))

            if len(effect) == 0:
                message = "Spell {}: contains empty effect"
                errors.append(message.format(spell["name"]))
            elif not all(e == effect[0] for e in effect) and "/".join(
                 map(str, effect)) != string_effect:
                message = "Spell {}: effect does not match effectBurn. "
                message += "{} is inconsistent with {}"
                errors.append(message.format(
                    spell["name"], effects, string_effects))

    return errors
