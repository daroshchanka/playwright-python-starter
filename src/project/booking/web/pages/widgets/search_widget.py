import json
import logging

from core.web.base_web_page import BaseWebPage
from core.web.ui_element import UiElement as el

log = logging.getLogger()


class SearchWidget(BaseWebPage):
    destination_container = el.by_test_id('destination-container')
    destination_input = el.by_xpath(f"{destination_container}//input")
    dates_container = el.by_test_id('searchbox-dates-container')
    dates_container_button = el.by_xpath(f"{dates_container}//button")
    dates_container_calendar = el.by_id('calendar-searchboxdatepicker')
    occupancy_config_button = el.by_test_id('occupancy-config')
    occupancy_config_popup = el.by_test_id('occupancy-popup')
    occupancy_config_popup_done_button = el.by_xpath(f"{occupancy_config_popup}/button")
    occupancy_config_adults_input = el.by_id('group_adults')
    occupancy_config_adults_decrement_icon = el.by_xpath(f"{occupancy_config_adults_input}/..//button[1]")
    occupancy_config_adults_increment_icon = el.by_xpath(f"{occupancy_config_adults_input}/..//button[2]")
    occupancy_config_children_input = el.by_id('group_children')
    occupancy_config_children_decrement_icon = el.by_xpath(f"{occupancy_config_children_input}/..//button[1]")
    occupancy_config_children_increment_icon = el.by_xpath(f"{occupancy_config_children_input}/..//button[2]")
    occupancy_config_rooms_input = el.by_id('no_rooms')
    occupancy_config_rooms_decrement_icon = el.by_xpath(f"{occupancy_config_rooms_input}/..//button[1]")
    occupancy_config_rooms_increment_icon = el.by_xpath(f"{occupancy_config_rooms_input}/..//button[2]")
    occupancy_pets_checkbox_hidden = el.by_xpath("//input[@type='checkbox'][@name='pets']")
    occupancy_pets_checkbox_switcher = el.by_xpath("//label[@for='pets']//span[1]")
    search_submit_button = el.by_xpath("//div[(contains(@class, 'hero-banner-searchbox')) or "
                                       "(@data-testid='searchbox-layout-wide')]//button[@type='submit']")

    def get_destination_autocomplete_result(self, number: int) -> el:
        return el.by_xpath(f"(//li[contains(@id, 'autocomplete-result-')])[{number}]")

    def get_dates_container_calendar_month(self, number: int) -> el:
        return el.by_xpath(f"({self.dates_container_calendar}//table)[{number}]")

    def get_datepicker_day(self, day_number: int, calendar_month: int) -> el:
        return el.by_xpath(
            f"({self.get_dates_container_calendar_month(calendar_month)}//td[@role='gridcell']/span)[{day_number}]")

    def get_flexible_days_option(self, option: str | int) -> el:
        return el.by_xpath(f"//*[@data-testid='flexible-dates-container']//input[@value={option}]/..")

    def get_occupancy_config_child_age_dropdown(self, number: int) -> el:
        return el.by_xpath(f"(//select[@name='age'])[{number}]")

    def is_loaded(self) -> bool:
        return self.destination_container.is_visible(self.page)

    def do_search(self, query: dict[str:any]):
        log.info(f"Do search {json.dumps(query)}")
        if query.get('where'):
            self.fill_where(query.get('where'))
        if query.get('when'):
            self.fill_when(query.get('when'))
        if query.get('occupancy'):
            self.fill_occupancy(query.get('occupancy'))
        self.search_submit_button.click(self.page)
        self.wait_for_network_idle()

    def fill_where(self, where: str):
        self.destination_container.click(self.page)
        self.destination_input.fill(self.page, where)
        self.pause(500)
        self.get_destination_autocomplete_result(1).click(self.page)

    def fill_when(self, when: dict[str:any]):
        if not self.dates_container.is_visible(self.page):
            self.dates_container_button.click(self.page)
        if when.get('flexibility'):
            self.get_flexible_days_option(when.get('flexibility')).click(self.page)
        from_month = 2 if when.get('from').get('month') == 'next' else 1
        self.get_datepicker_day(when.get('from').get('day'), from_month).click(self.page)
        to_month = 2 if when.get('to').get('month') == 'next' else 1
        self.get_datepicker_day(when.get('to').get('day'), to_month).click(self.page)

    def fill_occupancy(self, occupancy: dict[str:any]):
        if not self.occupancy_config_popup.is_visible(self.page):
            self.occupancy_config_button.click(self.page)
        self.__adjust_value_for_occupancy(
            occupancy.get('adults'),
            self.occupancy_config_adults_input,
            self.occupancy_config_adults_decrement_icon,
            self.occupancy_config_adults_increment_icon
        )
        children_list = occupancy.get('children')
        if children_list:
            children_count = len(children_list)
            log.debug(f'Children count {children_count}')
            log.debug(f'Children {json.dumps(children_list)}')
            self.__adjust_value_for_occupancy(
                children_count,
                self.occupancy_config_children_input,
                self.occupancy_config_children_decrement_icon,
                self.occupancy_config_children_increment_icon
            )
            for i in range(children_count):
                self.get_occupancy_config_child_age_dropdown(i + 1).set_option(self.page, [str(children_list[i])])
        self.__adjust_value_for_occupancy(
            occupancy.get('rooms'),
            self.occupancy_config_rooms_input,
            self.occupancy_config_rooms_decrement_icon,
            self.occupancy_config_rooms_increment_icon
        )
        if occupancy.get('pets') is True:
            if not self.occupancy_pets_checkbox_hidden.is_checked(self.page):
                self.occupancy_pets_checkbox_switcher.click(self.page)
        elif occupancy.get('pets') is False:
            if self.occupancy_pets_checkbox_hidden.is_checked(self.page):
                self.occupancy_pets_checkbox_switcher.click(self.page)
        self.occupancy_config_popup_done_button.click(self.page)

    def __adjust_value_for_occupancy(self, target_value: int | None, input_: el, decrement: el, increment: el):
        if target_value:
            current_value = int(input_.get_attribute(self.page, 'value'))
            value_delta = target_value - current_value
            change_value_icon = increment if value_delta > 0 else decrement
            log.debug(f"Set[{input}] value {current_value} -> {target_value}")
            for i in range(abs(value_delta)):
                change_value_icon.click(self.page)
