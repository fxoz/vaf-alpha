import atexit
from functools import cache
from camoufox.sync_api import Camoufox

import config


@cache
def browser():
    cm = Camoufox(headless=config.BROWSE_HEADLESS)
    b = cm.start()
    atexit.register(b.close)
    return b


@cache
def context():
    return browser().new_context()


@cache
def page():
    p = context().new_page()
    atexit.register(p.close)
    return p


def open_page(url: str):
    p = page()
    p.goto(url)
    return p
