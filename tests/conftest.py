import logging, pytest
from typing import Generator

import allure
from faker import Faker
from playwright.sync_api import Page, Playwright, APIRequestContext
from slugify import slugify

from core.playwright_config import PlaywrightConfig

logging.getLogger("faker").setLevel(logging.ERROR)
logging.getLogger("asyncio").setLevel(logging.ERROR)

log = logging.getLogger()
faker_ = Faker()


def pytest_addoption(parser):
    parser.addoption("--ENV", default="dev", help="ENV value for run tests: [dev, qa, stage]")
    parser.addoption("--project", action="store", default="chromium",
                     help="project value for run tests from conf/playwright_config.yaml")
    parser.addoption("--attach-screenshots", default="only-on-failure",
                     help="if screenshots will be attached to test report: [on, off, only-on-failure]")
    parser.addoption("--screenshot-mode", default="viewport", help="screenshot mode: [viewport, full]")


@pytest.fixture(scope="session", autouse=True)
def playwright_cli_configs(pytestconfig) -> dict[str:any]:
    return {
        'env': pytestconfig.getoption('--ENV'),
        'project': pytestconfig.getoption('--project'),
        'attach_screenshots': pytestconfig.getoption('--attach-screenshots'),
        'screenshot_mode': pytestconfig.getoption('--screenshot-mode'),
    }


@pytest.fixture(scope="session")
def playwright_configs(playwright_cli_configs) -> PlaywrightConfig:
    return PlaywrightConfig(playwright_cli_configs['project'])


@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig, playwright_configs):
    if len(pytestconfig.getoption('--browser', None)) > 0:
        log.warning("--browser option value is IGNORED, consider using --project")
    if pytestconfig.getoption('--browser-channel', None) is not None:
        log.warning("--browser-channel option value is IGNORED, consider using --project")
    for i in ['--tracing', '--video', '--screenshot', '--full-page-screenshot']:
        if pytestconfig.getoption(i, None) not in ['off', False]:
            log.warning(
                f"NOTE: {i}:{pytestconfig.getoption(i, None)} option value will not cause the data attached to Allure report, "
                f"data will be collected separately, "
                f"use --attach-screenshots, --screenshot-mode to manage Allure attachments")
    loaded_launch_args = playwright_configs.get_launch_args()
    if pytestconfig.getoption('--headed'):
        loaded_launch_args['headless'] = False
    slowmo_option = pytestconfig.getoption("--slowmo")
    if slowmo_option:
        loaded_launch_args['slow_mo'] = slowmo_option
    opts = {
        **loaded_launch_args
    }
    log.debug(f"browser_type_launch_args:{opts}")
    return opts


@pytest.fixture(scope="session")
def browser_context_args(playwright_configs, pytestconfig):
    if pytestconfig.getoption('--device') is not None:
        log.warning("--device option value is IGNORED, consider using --project to configure browser_context_args")
    loaded_browser_context_args = playwright_configs.get_browser_context_args()
    opts = {
        **loaded_browser_context_args,
    }
    log.debug(f"browser_context_args:{opts}")
    return opts


def allure_attach_screenshot(page: Page, full_page: bool):
    allure.attach(
        page.screenshot(type='png', full_page=full_page),
        name=f"{slugify(faker_.uuid4(cast_to=str))}.png",
        attachment_type=allure.attachment_type.PNG
    )


@pytest.hookimpl
def pytest_runtest_makereport(item, call) -> None:
    if 'playwright_cli_configs' in item.funcargs:
        playwright_cli_configs = item.funcargs['playwright_cli_configs']
        attach_screenshots = playwright_cli_configs['attach_screenshots']
        is_full_page = playwright_cli_configs['screenshot_mode'] == 'full'
        if attach_screenshots == 'on':
            if call.when == 'call' and 'page' in item.funcargs:
                page: Page = item.funcargs['page']
                allure_attach_screenshot(page, is_full_page)
        elif attach_screenshots == 'only-on-failure':
            if call.excinfo is not None and 'page' in item.funcargs:
                page: Page = item.funcargs['page']
                allure_attach_screenshot(page, is_full_page)


@pytest.fixture(scope="session")
def api_context_args(request) -> dict[str, any]:
    opts = {}
    log.info(f"api_context_args:{opts}")
    return opts


@pytest.fixture(scope="session")
def api_request(playwright: Playwright, api_context_args) -> Generator[
    APIRequestContext, None, None]:
    request_context = playwright.request.new_context(**api_context_args)
    yield request_context
    request_context.dispose()