import logging
from typing import Self

from playwright.sync_api import Page

from core.web.base_web_page import BaseWebPage
from core.web.ui_element import UiElement as el
from project.booking.web.pages.widgets.search_widget import SearchWidget
from project.booking.web.pages.widgets.top_header_widget import TopHeaderWidget

log = logging.getLogger()


class SearchResultsPage(BaseWebPage):
    assertive_header = el.by_xpath("//h1[@aria-live='assertive']")
    map_trigger = el.by_xpath("//div[contains(@data-testid, 'map-trigger')]")
    search_result_item = el.by_test_id('property-card')

    top_header: TopHeaderWidget
    search: SearchWidget

    def __init__(self, page: Page):
        super().__init__(page)
        self.top_header = TopHeaderWidget(page)
        self.search = SearchWidget(page)

    def is_loaded(self) -> bool:
        result = self.assertive_header.is_visible(self.page) and self.map_trigger.is_visible(self.page)
        log.info(f"Check SearchResults page is loaded - {result}")
        return result

    def get_assertive_header_text(self) -> str:
        result = self.assertive_header.get_text(self.page)
        log.info(f"Get assertive header text - {result}")
        return result

    def get_search_result_cards_count(self) -> int:
        result = len(self.search_result_item.get_list(self.page))
        log.info(f"Get search results visible cards count - {result}")
        return result

    def do_search(self, query) -> Self:
        self.search.do_search(query)
        return self
