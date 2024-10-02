import re
from datetime import datetime

from playwright.sync_api import Page

from project.booking.web.pages.landing_page import LandingPage
from project.booking.web.pages.search_results_page import SearchResultsPage


def test_simple_search_query(page: Page):
    landing_page = LandingPage(page)
    landing_page.navigate()
    assert landing_page.is_loaded()

    search_query = {
        'where': 'London',
        'when': {
            'from': {'day': 7, 'month': 'next'},
            'to': {'day': 21, 'month': 'next'},
        }
    }

    landing_page.do_search(search_query)
    search_results_page = SearchResultsPage(page)
    assert search_results_page.is_loaded()
    assert search_results_page.get_search_result_cards_count() >= 25
    assert re.search(f"{search_query['where']}: \\d,\\d+ properties found",
                     search_results_page.get_assertive_header_text())


def test_complex_search_query(page: Page):
    landing_page = LandingPage(page)
    landing_page.navigate()
    assert landing_page.is_loaded()

    search_query = {
        'where': 'Iceland',
        'when': {
            'from': {'day': datetime.now().day, 'month': 'current'},
            'to': {'day': 15, 'month': 'next'},
            'flexibility': '7',
        },
        'occupancy': {
            'adults': 1,
            'children': [0, 7, 17],
            'rooms': 2,
            'pets': True,
        },
    }

    landing_page.do_search(search_query)
    search_results_page = SearchResultsPage(page)
    assert search_results_page.is_loaded()
    assert search_results_page.get_search_result_cards_count() <= 25
    assert re.search(f"{search_query['where']}: \\d+ properties found", search_results_page.get_assertive_header_text())

    search_query_2 = {
        'occupancy': {
            'pets': False,
        },
    }
    search_results_page.do_search(search_query_2)
    assert search_results_page.get_search_result_cards_count() >= 25
    assert re.search(f"{search_query['where']}: \\d+ properties found", search_results_page.get_assertive_header_text())
