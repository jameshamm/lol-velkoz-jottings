"""Command to test various different data sets.

The data sets with tests current are
    Items
"""
import click

from ..tests import run_intra_champion_tests
from ..data import DataManager, compress_name


@click.command()
@click.option(
    '--all-items', is_flag=True, help="Run the tests on all items.")
@click.option(
    '--all-champions', is_flag=True,
    help="Run the tests on all (known) champions. This does not work in "
    "conjunction with the option for specific champions.")
@click.option(
    '-c', '--champion', '--champions', multiple=True,
    metavar='<Champion name>', help="A specific champion to run tests on.")
def test(champions, all_champions, all_items):
    """Run tests on various data sets."""
    click.echo("Tests are still being made.")

    # Make sure either some champions or all champions are selected.
    # Both is not allowed.
    if champions and all_champions:
        raise click.BadOptionUsage(
            "The options for both individual champions and "
            "all champions were set. Please only use one of those options")

    manager = DataManager()

    if champions or all_champions:
        known_champions = manager.all_champion_names()

        if all_champions:
            click.echo("Running tests on all champions.")
            click.echo("=" * 12)
            champions = known_champions.values()

        if champions:
            # Validate the champion names passed in.
            unknown_champions = [
                champion for champion in champions
                if compress_name(champion) not in known_champions]

            if unknown_champions:
                message = "Some champion are not known: {}.".format(
                    unknown_champions)
                raise ValueError(message)

            # Make sure each name is in the right format to look it up.
            # E.g. kog'maw -> KogMaw, cho'gath -> Chogath
            champions = [
                known_champions[compress_name(name)] for name in champions]

            # Finally run tests
            for champion in sorted(champions):
                run_intra_champion_tests(champion)

    if all_items:
        click.echo("The data set with all items is not supported yet.")
