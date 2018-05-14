"""log.py controls how messages are printed.

It is essentially a custom logger, so beware. :P
No effort has been made to make this threadsafe."""
ANSI_COLOUR_CODES = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "reset": "\033[0m"
}

DISABLE_COLOUR = False


def _no_colour(colour):
    """Return True if no colour should be included in any output."""
    return DISABLE_COLOUR or colour.lower() not in ANSI_COLOUR_CODES


def log(*contents, name=None, colour=None, **kwargs):
    """Print a message (maybe in colour) with some formatting."""
    if name is None:
        name = ""
    else:
        name = "[" + name + "]: "

    if colour is None or _no_colour(colour):
        colour_code = ""
        reset = ""
    else:
        colour_code = ANSI_COLOUR_CODES[colour.lower()]
        reset = ANSI_COLOUR_CODES["reset"]

    message = "{}{}{}{}"
    print(message.format(colour_code, name, reset, *contents), **kwargs)


def info(*args, **kwargs):
    """Display an informative message."""
    log(*args, name="INFO", **kwargs)


def fail(*args, **kwargs):
    """Display a message about a failure."""
    log(*args, name="FAIL", colour="red", **kwargs)


def success(*args, **kwargs):
    """Display a message about a success."""
    log(*args, name="SUCCESS", colour="green", **kwargs)


def warning(*args, **kwargs):
    """Display a message about a warning."""
    log(*args, name="WARNING", colour="yellow", **kwargs)


def count(message, current_iteration, total):
    """Display the current test information out of a total"""
    # The space needed to pad the current iteration.
    left_padding = len(str(total))
    progress = "{:>{}}/{} - ".format(current_iteration, left_padding, total)
    log(progress + message, name="TEST")


def test_result(message, errors, indent=4):
    """Display the test information as given, with nice indentation."""
    if errors:
        ending = "issues" if len(errors) != 1 else "issue"
        fail(message + " - {} {}".format(len(errors), ending))

        indent_str = " " * indent
        for error in errors:
            log(indent_str + error)
    else:
        success(message)
