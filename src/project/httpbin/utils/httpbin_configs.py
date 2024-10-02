import logging
from configparser import ConfigParser

log = logging.getLogger()


class HttpbinConfigs:
    def __init__(self, env_name):
        self.env_name = env_name
        log.info(f'read configs for --ENV={env_name}')
        self.config = ConfigParser()
        self.config.read(
            [
                'conf/httpbin.ini',
                '../conf/httpbin.ini', #to work when run tests from IDE
            ]
        )

    def api_base_url(self):
        result = self.config.get(self.env_name, 'api_base_url')
        log.debug(f'read config[api_base_url]={result}')
        return result

    def web_base_url(self):
        result = self.config.get(self.env_name, 'web_base_url')
        log.debug(f'read config[web_base_url]={result}')
        return result
