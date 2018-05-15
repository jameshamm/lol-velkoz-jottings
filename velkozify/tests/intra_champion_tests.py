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
            values, values_string = spell[attribute], spell[attribute + "Burn"]

            if not list_and_str_match(values, values_string):
                message = "Spell {}: {} does not match {}. "
                message += "{} is inconsistent with {}"

                errors.append(message.format(
                    spell["name"], attribute, attribute + "Burn",
                    values, values_string))

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
                    spell["name"], effect, effect_string))

    return errors


def list_and_str_match(values, values_string):
    """Return True if the list of values and the string of the values match

    There are two cases
    1) The values are all the same and the string is a single value
    list_and_str_match([0, 0, 0], '0') -> True

    2) The values are different and the string reflects that
    list_and_str_match([50, 100, 150], '50/100/150') -> True

    NOTE: An issue arises due to floating point error and
    rounding to two places. There are 'inconsistencies' in the data set.
    0.015 -> 0.01
    0.002 -> 0.0
    0.0286 -> 0.03
    To solve this we rolled a custom _close function that is pretty imprecise.
    """
    if all(value == values[0] for value in values) and \
       _close(values[0], float(values_string)):
        return True

    return "/".join(map(str, values)) == values_string


def _close(one, two, abs_diff=0.0051):
    """A worse math.isclose. This could probably be done with isclose instead.

    The default is 0.0051 because 0.005 doesn't catch all the 'differences'.

    >>> isclose(0.015, 0.01) -> False
    >>> _close(0.015, 0.01) -> True"""
    return abs(one - two) <= abs_diff
