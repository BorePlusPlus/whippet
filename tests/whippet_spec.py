from whippet import __version__, whippet


def it_exposes_version():
    assert __version__ == "0.1.0"


def it_increments():
    assert whippet.inc(1) == 2
