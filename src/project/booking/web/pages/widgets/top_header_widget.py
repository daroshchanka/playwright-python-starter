import logging

from core.web.base_web_page import BaseWebPage
from core.web.ui_element import UiElement as el

log = logging.getLogger()


class TopHeaderWidget(BaseWebPage):
    header_logo = el.by_test_id('header-logo')
    user_currency_picker_icon = el.by_test_id('header-currency-picker-trigger')
    user_language_picker_icon = el.by_test_id('header-language-picker-trigger')
    sign_up_button = el.by_test_id('header-sign-up-button')
    sign_in_button = el.by_test_id('header-sign-in-button')
    navigation_menu = el.by_test_id('header-xpb')
    navigation_menu_accommodations = el.by_xpath(f"{user_currency_picker_icon}//a[@id='accommodations']")
    navigation_menu_flights = el.by_xpath(f"{user_currency_picker_icon}//a[@id='flights']")
    navigation_menu_attractions = el.by_xpath(f"{user_currency_picker_icon}//a[@id='attractions']")
    navigation_menu_airport_taxis = el.by_xpath(f"{user_currency_picker_icon}//a[@id='airport_taxis']")

    def is_loaded(self) -> bool:
        return (
                self.header_logo.is_visible(self.page) and
                self.user_language_picker_icon.is_visible(self.page) and
                self.navigation_menu_accommodations.is_visible(self.page)
        )
