"""The commands to show information about the data sets.

Examples of useful information include:
    What is the latest patch?
    How many champions exist in patch 8.4?
"""
import click


@click.command()
def info():
    """Show information about various data sets."""
    click.echo("Info is still under development")
