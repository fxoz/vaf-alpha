from rich import print

from . import browser


def _get_element(role: str, name: str):
    page = browser.page()
    return page.get_by_role(role, name=name)


def click(role: str, name: str) -> None:
    ele = _get_element(role, name)
    ele.click()


def select_and_type_text(
    role: str, name: str, text_to_type: str, press_enter_after: bool
) -> None:
    ele = _get_element(role, name)
    ele.click()
    ele.type(text_to_type)

    if press_enter_after:
        ele.press("Enter")
