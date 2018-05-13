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


def log(*contents, name=None, colour=None, **kwargs):
    """Print a message in colour with some extra info."""
    if name is None:
        name = ""
    else:
        name = "[" + name + "]: "

    if colour is None or DISABLE_COLOUR or colour.lower() not in ANSI_COLOUR_CODES:
        colour_code = ""
        reset = ""
    else:
        colour_code = ANSI_COLOUR_CODES[colour.lower()]
        reset = ANSI_COLOUR_CODES["reset"]

    message = "{}{}{}{}"
    print(message.format(colour_code, name, reset, *contents), **kwargs)


def info(*args, **kwargs):
    log(*args, name="INFO", **kwargs)


def fail(*args, **kwargs):
    log(*args, name="FAIL", colour="red", **kwargs)


def success(*args, **kwargs):
    log(*args, name="SUCCESS", colour="green", **kwargs)


def warning(*args, **kwargs):
    log(*args, name="WARNING", colour="yellow", **kwargs)
