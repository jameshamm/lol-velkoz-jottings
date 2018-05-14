"""intra_champion_tests.py contains tests that check the internal consistency
of a champion's data.

All test will be named in the format test_*
"""
from ..logger import log


def run_intra_champion_tests(manager, champion_name):
    """Run the tests for the supplied champion."""
    champion_data = manager.get_data(champion_name)

    spell_errors = test_champion_spells(champion_name, champion_data)
    if spell_errors:
        message = "Error inside {}".format(champion_name)
        log.test_result(message, spell_errors)


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
        effects, effects_strings = spell["effect"], spell["effectBurn"]
        if len(effects) != len(effects_strings):
            message = "Spell {}: effect does not match effectBurn. "
            message += "len({}) != len({})"
            errors.append(message.format(
                spell["name"], effects, effects_strings))

        for effect, effect_string in zip(effects, effects_strings):
            # Skip any null entries.
            if effect is None and effect_string is None:
                continue

            if len(effect) != spell["maxrank"]:
                message = "Spell {}: effect does not match maxrank. "
                message += "len({}) != {}"
                errors.append(message.format(
                    spell["name"], effect, spell["maxrank"]))

            if not effect:
                message = "Spell {}: contains empty effect"
                errors.append(message.format(spell["name"]))
            elif not list_and_str_match(effect, effect_string):
                message = "Spell {}: effect does not match effectBurn. "
                message += "{} is inconsistent with {}"
                errors.append(message.format(
                    spell["name"], effects, effects_strings))

    return errors


def list_and_str_match(effect, effect_string):
    """TODO: Move other items to this function"""
    if not all(e == effect[0] for e in effect):
        return False

    return "/".join(map(str, effect)) != effect_string
