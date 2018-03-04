"""The main entrypoint for commands."""
import click

from .commands import info, test


@click.group()
@click.option('--json-output', is_flag=True)
def main(json_output):
    """A tool to test and analyse league of legends data sets."""
    if json_output:
        click.echo("Outputing in json has not been implemented yet.")
    click.echo("Hello, void!")


main.add_command(test)
main.add_command(info)
