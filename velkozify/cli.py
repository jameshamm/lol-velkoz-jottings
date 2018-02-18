import click


@click.command()
@click.option('--all-champions', is_flag=True)
@click.option('--all-items', is_flag=True)
def main(all_champions, all_items):
    if all_champions:
        click.echo("Checks for all champions are not implemented yet.")

    if all_items:
        click.echo("Checks for all items are not implemented yet.")
    click.echo("hello, void!")
