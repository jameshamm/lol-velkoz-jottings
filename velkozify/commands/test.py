"""Command to test various different data sets.

The data sets with tests current are
    Champions
    Items
"""

from ..tests import run_intra_champion_tests, run_champion_itemsets_tests, run_item_paths_tests, run_intra_item_tests
from ..data import DataManager, compress_name
from ..logger import log


def test_champions(manager, champions=None):
    """Run test for the passed champions.
    Data will be sourced from the Data Manager."""
    log.info("Testing champs is still in development!")
    known_champions = manager.all_champion_names()

    if champions is None:
        champions = known_champions.values()
    else:
        # Validate the champion names passed in.
        # TODO: Move this validation step to the type argument.
        compressed_champions_names = [
            compress_name(champion) for champion in champions]

        unknown_champions = [
            champion
            for champion in compressed_champions_names
            if champion not in known_champions]

        if unknown_champions:
            message = "Some champion are not known: {}.".format(
                unknown_champions)
            raise ValueError(message)

        # Make sure each name is in the right format to look it up.
        # E.g. kog'maw -> KogMaw, cho'gath -> Chogath
        champions = [
            known_champions[name] for name in compressed_champions_names]

    # Run the tests.
    for i, champion in enumerate(sorted(champions), 1):
        log.count(f"Running tests on {champion}", i, len(champions))
        run_intra_champion_tests(manager, champion)
        run_champion_itemsets_tests(manager, champion)

    log.info("Done testing champions.")


def test_items(manager, items=None):
    """Run test for items.
    Data will be sourced from the supplied Data Manager."""
    log.info("Testing items is still in development!")
    if items is None:
        # Testing all items
        log.info("Running tests on all items.")
        item_ids = manager.get_data(all_items=True)['data'].keys()

        for i, item_id in enumerate(sorted(item_ids), 1):
            log.count(f"Running tests on {item_id}", i, len(item_ids))
            run_item_paths_tests(manager, item_id)
            run_intra_item_tests(manager, item_id)
    else:
        log.info("Specific item tests are not ready.")
    log.info("Done with items.")


def test_runner(args):
    """Run either the champion tests or the items tests."""
    manager = DataManager(args.patch)

    if args.all_champions or args.champions:
        test_champions(manager, args.champions)
    elif args.all_items or args.items:
        test_items(manager, args.items)
    else:
        # Something went wrong
        raise ValueError(f"Something unexpected happened with {args}")


def setup_test_parser(parser):
    """Add the arguments to the parser for the 'test' command."""
    test_args = parser.add_mutually_exclusive_group(required=True)
    # Test champions.
    test_args.add_argument(
        '--champions', metavar="<champion name>", nargs='+', type=str)
    test_args.add_argument(
        '--all-champions', action="store_true", help="Run the tests on all (known) champions")

    # Or test items.
    test_args.add_argument(
        '--items', metavar="<item name>", nargs='+', type=str)
    test_args.add_argument(
        '--all-items', action="store_true", help="Run the tests on all items.")

    parser.set_defaults(run=test_runner)
