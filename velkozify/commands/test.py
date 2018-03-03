"""Command to test various different data sets.

The data sets with tests current are
    Items
"""
import click


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

    # Make sure either some champions or all champions is picked.
    # Both is not allowed.
    if champions and all_champions:
        raise click.BadOptionUsage(
            "The options for both individual champions and "
            "all champions were set. Please only use one of those options")

    if champions:
        click.echo("The champs named are: " + str(champions))

    if all_champions:
        click.echo("Running tests for all champions is not supported yet.")
