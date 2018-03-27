"""The commands to show information about the data sets.

Examples of useful information include:
    What is the latest patch?
    How many champions exist in patch 8.4?
"""
def setup_info_parser(parser):
    """Add the arguments to the parser for the 'test' command."""
    parser.set_defaults(command=lambda args: print(f"Saw these args {args}"))
