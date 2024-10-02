import logging
from typing import Self

from playwright.sync_api import Page, Frame, Locator

log = logging.getLogger()


class UiElement:
    locator: str

    def __init__(self, xpath: str):
        self.locator = xpath

    def __str__(self):
        return self.locator

    @classmethod
    def by_test_id(cls, test_id: str) -> Self:
        return cls(f"//*[@data-testid='{test_id}']")

    @classmethod
    def by_id(cls, id_: str) -> Self:
        return cls(f"//*[@id='{id_}']")

    @classmethod
    def by_xpath(cls, xpath: str) -> Self:
        return cls(xpath)

    def get(self, pof: Page | Frame) -> Locator:
        return pof.locator(f"xpath={self.locator}").first

    def is_visible(self, pof: Page | Frame) -> bool:
        result = self.get(pof).is_visible()
        log.debug(f"{self.locator} is_visible - {result}")
        return result

    def is_checked(self, pof: Page | Frame) -> bool:
        result = self.get(pof).is_checked()
        log.debug(f"{self.locator} is_checked - {result}")
        return result

    def get_text(self, pof: Page | Frame) -> str:
        result = self.get(pof).text_content()
        log.debug(f"{self.locator} get_text - {result}")
        return result

    def get_attribute(self, pof: Page | Frame, attr_name: str) -> str:
        result = self.get(pof).get_attribute(attr_name)
        log.debug(f"{self.locator} get_attribute - {result}")
        return result

    def wait_for_visible(self, pof: Page | Frame, timeout_sec: int = 10):
        log.debug(f"{self.locator} wait_for_visible - {timeout_sec} sec")
        self.get(pof).wait_for(state='visible', timeout=timeout_sec * 1000)

    def wait_for_attached(self, pof: Page | Frame, timeout_sec: int = 10):
        log.debug(f"{self.locator} wait_for_attached - {timeout_sec} sec")
        self.get(pof).wait_for(state='attached', timeout=timeout_sec * 1000)

    def wait_for_detached(self, pof: Page | Frame, timeout_sec: int = 10):
        log.debug(f"{self.locator} wait_for_detached - {timeout_sec} sec")
        self.get(pof).wait_for(state='detached', timeout=timeout_sec * 1000)

    def click(self, pof: Page | Frame):
        log.debug(f"{self.locator} click")
        self.get(pof).click()

    def clear(self, pof: Page | Frame):
        log.debug(f"{self.locator} clear")
        self.get(pof).clear()

    def fill(self, pof: Page | Frame, text: str):
        log.debug(f"{self.locator} fill({text})")
        element = self.get(pof)
        element.fill(text)

    def set_option(self, pof: Page | Frame, options: list[str]):
        log.debug(f"{self.locator} set_option({options})")
        self.get(pof).select_option(options)

    def get_list(self, pof: Page | Frame) -> list[Self]:
        count = pof.locator(f"xpath={self.locator}").count()
        result = []
        for e in range(count):
            result.append(UiElement(f"({self.locator})[{e + 1}]"))
        log.debug(f"{self.locator} get_list, found - {count}")
        return result
