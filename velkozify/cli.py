"""The main entrypoint for commands."""
import argparse

from .commands.test import setup_test_parser
from .commands.info import setup_info_parser
from .data import DataManager, get_latest_patch


def main():
    """The main entrypoint for the cli."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--patch', default="latest", help="The patch to source data from.")

    # TODO: Add type to guarantee the patch is valid.
    # TODO: Add choices and a nice help format to display possible patches
    # (including the latest patch).
    subcommands = parser.add_subparsers(title="Commands")

    test_parser = subcommands.add_parser('test')
    setup_test_parser(test_parser)

    info_parser = subcommands.add_parser('info')
    setup_info_parser(info_parser)

    args = parser.parse_args()

    if args.patch.lower() == "latest":
        patch = get_latest_patch()

    manager = DataManager(patch)

    args.run_tests(manager, args)

    print("Done")
