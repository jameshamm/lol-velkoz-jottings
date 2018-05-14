"""The commands to show information about the data sets.

Examples of useful information include:
    What is the latest patch?
    How many champions exist in patch 8.4?
"""
from ..data import DataManager, get_latest_patch


def compare_data(new_data, old_data, name=""):
    # print(new_data, old_data)
    # TODO: This seems buggy, replace it with a proper differ.
    are_different = False
    if not isinstance(old_data, dict):
        if not isinstance(old_data, (list, tuple)):
            if old_data != new_data:
                print("Values differ")
                if name:
                    print(name)
                print(new_data)
                print(old_data)
                print()
                return False
            return True

        if len(new_data) != len(old_data):
            print("Values differ in size")
            print(new_data)
            print(old_data)
            print()
            return False

        # print(new_data, old_data)
        return any(compare_data(new, old, name) for new, old in zip(new_data, old_data))

    for key, old_value in old_data.items():
        if key == "version":
            # We already know the patches will differ.
            continue

        if key not in new_data:
            print(f"Missing key: {key}")
            print()
            are_different = True
            continue

        new_value = new_data[key]
        if isinstance(old_value, (dict, list, tuple)):
            if type(new_value) != type(old_value):
                print("Values differ in type")
                print(new_value)
                print(old_value)
                print()
                are_different = True
            else:
                if compare_data(new_value, old_value, name + "-" + key):
                    are_different = True
        elif old_value != new_value:
            print("Values differ")
            if name:
                print(name + "-" + key)
            print(new_value)
            print(old_value)
            print()
            are_different = True

    for key, new_value in new_data.items():
        if key not in old_data:
            print(f"New data under {key}")
            print(new_value)
            print()
            are_different = True

    return are_different


def get_diff(args):
    champion = args.champion
    new_patch, old_patch = args.new_patch, args.old_patch
    if new_patch.lower() == "latest":
        new_patch = get_latest_patch()

    if old_patch.lower() == "latest":
        old_patch = get_latest_patch()

    if new_patch == old_patch:
        raise ValueError("The supplied patches are the same?")

    new_data = DataManager(new_patch).get_data(champion)
    old_data = DataManager(old_patch).get_data(champion)

    compare_data(new_data, old_data)

    # TODO: Finish this.


def get_info(args):
    print(args)


def setup_info_parser(parser):
    """Add the arguments to the parser for the 'test' command."""
    subcommands = parser.add_subparsers(title="Information")

    diff_parser = subcommands.add_parser("diff")
    diff_parser.add_argument(
        'champion', metavar="<champion name>", type=str
    )
    diff_parser.add_argument(
        'new_patch', nargs="?", default="latest"
    )
    diff_parser.add_argument(
        'old_patch', type=str
    )

    diff_parser.set_defaults(run=get_diff)

    parser.set_defaults(run=get_info)
