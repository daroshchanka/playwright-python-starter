import pytest, logging

from project.httpbin.utils.httpbin_configs import HttpbinConfigs

log = logging.getLogger()


@pytest.fixture(scope="session")
def project_configs(playwright_cli_configs) -> HttpbinConfigs:
    return HttpbinConfigs(playwright_cli_configs['env'])


@pytest.fixture(scope="session")
def api_context_args(api_context_args, project_configs: HttpbinConfigs) -> dict[str, any]:
    opts = {
        **api_context_args,
        'base_url': project_configs.api_base_url()
    }
    log.info(f"api_context_args:{opts}")
    return opts

