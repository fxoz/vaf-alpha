import argparse

from typing import Optional
from camoufox.sync_api import Camoufox

import config


def fetch_aria_tree(
    *,
    url: Optional[str] = None,
    headless: bool = True,
) -> str:
    with Camoufox(headless=headless) as browser:
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")

        return page.locator("body").aria_snapshot()


def main() -> None:
    print(
        fetch_aria_tree(
            url="https://wetteronline.de",
            headless=True,
        )
    )


if __name__ == "__main__":
    main()
