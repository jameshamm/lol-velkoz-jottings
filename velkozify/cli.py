import click

from .commands import info, test


@click.group()
@click.option('--json-output', is_flag=True)
def main(json_output):
    if json_output:
        click.echo("Outputing in json has not been implemented yet.")
    click.echo("hello, void!")


main.add_command(test)
main.add_command(info)
