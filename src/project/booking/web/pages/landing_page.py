import logging
from typing import Self

from playwright.sync_api import Page

from core.web.base_web_page import BaseWebPage
from core.web.ui_element import UiElement as el
from project.booking.web.pages.search_results_page import SearchResultsPage
from project.booking.web.pages.widgets.search_widget import SearchWidget
from project.booking.web.pages.widgets.top_header_widget import TopHeaderWidget

log = logging.getLogger()


class LandingPage(BaseWebPage):
    hero_banner = el.by_xpath("//div[contains(@class, 'hero-banner')]")
    promo_section = el.by_xpath("//div[contains(@class, 'promo-section')]")
    register_popup = el.by_xpath("//div[@role='dialog']")
    register_popup_close_icon = el.by_xpath(f"${register_popup}//button")
    mobile_view_header_menu = el.by_test_id('header-mobile-menu-button')
    mobile_view_menu_drawer = el.by_test_id('header-mobile-menu-modal')
    mobile_view_menu_drawer_close_button = el.by_test_id('header-mobile-menu-modal-close')
    mobile_view_menu_careers_item = el.by_xpath(
        f"{mobile_view_menu_drawer}//a[contains(@href, 'https://careers.booking.com')]")

    popup = el.by_xpath("(//div[@role='dialog'])[last()]")
    popup_close_icon = el.by_xpath(f"{popup}//button")

    top_header: TopHeaderWidget
    search: SearchWidget

    def __init__(self, page: Page):
        super().__init__(page)
        self.top_header = TopHeaderWidget(page)
        self.search = SearchWidget(page)

    def navigate(self) -> Self:
        log.info('Navigate to Landing page')
        self.page.goto('/')
        self.wait_for_network_idle()
        self.handle_popup()
        return self

    def is_loaded(self) -> bool:
        result = (
                self.hero_banner.is_visible(self.page) and
                self.promo_section.is_visible(self.page)
        )
        log.info(f"Check Landing page is loaded - {result}")
        return result

    def handle_popup(self):
        try:
            self.popup.wait_for_visible(self.page, 4)
            log.debug('Closing popup')
            self.popup_close_icon.click(self.page)
            self.popup.wait_for_detached(self.page)
        except:
            pass

    def do_search(self, query) -> Self:
        self.search.do_search(query)
        return self

    def is_mobile_view_loaded(self) -> bool:
        result = self.mobile_view_header_menu.is_visible(self.page)
        log.info(f"Check is Landing page Mobile view loaded - {result}")
        return result

    def open_mobile_menu(self) -> Self:
        log.info("Open mobile view top menu")
        self.mobile_view_header_menu.click(self.page)
        self.pause(500)
        return self

    def is_mobile_menu_opened(self) -> bool:
        result = self.mobile_view_menu_drawer.is_visible(self.page)
        log.info(f"Check is Mobile menu opened - {result}")
        return result

    def is_mobile_menu_careers_item_visible(self) -> bool:
        result = self.mobile_view_menu_careers_item.is_visible(self.page)
        log.info(f"Check is Mobile menu Careers item visible - {result}")
        return result

    def close_mobile_menu(self) -> Self:
        log.info('Close mobile view top menu')
        self.mobile_view_menu_drawer_close_button.click(self.page)
        self.mobile_view_menu_drawer_close_button.wait_for_detached(self.page)
        return self
