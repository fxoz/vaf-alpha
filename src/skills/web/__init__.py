from .._base import Skill

from . import banned
from . import scraper
from . import browser
from . import controller

from rich import print


def init_browser():
    browser.browser()


class WebSkill(Skill):
    def open_and_fetch_contents(self, url: str) -> str:
        """Run this before interacting with the page, like clicking or typing.."""
        url = url.replace("google.com/", "duckduckgo.com/")
        if banned.is_website_banned(url):
            raise ValueError(f"Browsing to {url} is not allowed!")

        return scraper.open_and_fetch_aria_tree(url)

    def fetch_current_contents(self) -> str:
        """Very useful after interactions, like submitting a form, clicking a link etc. to get the updated/new page contents."""
        return scraper.fetch_aria_tree()

    def click_element(self, role: str, name: str) -> None:
        """IMPORTANT! Fetch the contents of the page first, and determine the element to click!  `- list: - listitem: - link "Schweiz": - /url: /wetter/schweiz` -> element_type=\"link\", text=\"Schweiz\""""
        print(f"Clicking element of type {role} with name {name}")
        controller.click(role, name)

    def select_element_and_type_text(
        self, role: str, name: str, text_to_type: str, press_enter_after: bool
    ) -> None:
        """IMPORTANT! Fetch the contents of the page first, and determine the element to interact with!  `- group:  - textbox: Das Wetter in ...` -> element_type=\"textbox\", text=\"Das Wetter in ...\""""

        print(
            f"Selecting element of type {role} with name {name}, typing text: {text_to_type}, press_enter_after: {press_enter_after}"
        )
        controller.select_and_type_text(role, name, text_to_type, press_enter_after)
