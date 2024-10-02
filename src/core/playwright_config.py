import functools
import logging, yaml
import os

log = logging.getLogger()


class PlaywrightConfig:
    _CONFIG = None

    def __init__(self, browser: str):
        self.browser = browser

    @classmethod
    def read_config(cls):
        if getattr(cls, '_CONFIG', None) is None:
            valid_path = next(f for f in [
                'conf/playwright_config.yaml',
                '../conf/playwright_config.yaml', #to work when run tests from IDE
            ] if os.path.isfile(f))
            with open(valid_path, 'r') as file:
                config = yaml.safe_load(file)
            cls._CONFIG = config
        return cls._CONFIG

    @functools.cache
    def get_browser_configs(self) -> dict[str:any]:
        projects = list(self.read_config()['projects'])
        result = next((x for x in projects if x['name'] == self.browser), None)
        log.debug(f"looking for '{self.browser}' configs by 'name', found: {result is not None}")
        if result is None:
            result = next((x for x in projects if x['type'] == self.browser), None)
            log.debug(f"looking for '{self.browser}' configs by 'type', found: {result is not None}")
        if result is None:
            log.warning(f"configs for '{self.browser}' not found, use default: chrome")
            self.browser = 'chrome'
            result = next((x for x in projects if x['name'] == self.browser), None)
            log.debug(f"looking for '{self.browser}' configs by 'type', found: {result is not None}")
        assert result is not None
        return result

    def get_launch_args(self) -> dict[str:any]:
        return self.get_browser_configs()['launch_args']

    def get_browser_context_args(self) -> dict[str:any]:
        return self.get_browser_configs()['browser_context_args']
