import time
from rich import print

from . import browser


def fetch_aria_tree() -> str:
    page = browser.page()
    aria_tree = page.locator("body").aria_snapshot()

    with open(f"logs/{time.time():.2f}_aria_tree.yml", "w", encoding="utf-8") as f:
        f.write(str(aria_tree))

    return aria_tree


def open_and_fetch_aria_tree(url: str) -> str:
    start = time.time()

    browser.open_page(url)
    print(f"Page load time: {time.time() - start:.2f} seconds")

    return fetch_aria_tree()


if __name__ == "__main__":
    open_and_fetch_aria_tree("https://www.wetteronline.de/")
