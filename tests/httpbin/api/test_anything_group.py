import pytest, json, logging
from playwright.sync_api import APIRequestContext
from project.httpbin.api.services.anything_service import AnythingService
from project.httpbin.utils.data.anything_dto import AnythingDto
from project.httpbin.utils.data.generators.anything_generator import AnythingGenerator

log = logging.getLogger()


@pytest.fixture(scope="session")
def api_service(api_request: APIRequestContext) -> AnythingService:
    return AnythingService(api_request)


def test_get_anything(api_service: AnythingService):
    query = {'ids': '1,2,3', 'enabled': True}
    response = api_service.get_anything(query)
    assert response.status() == 200
    json_output = response.json()
    assert json_output['args']['ids'] == query['ids']
    assert json_output['args']['enabled'] == str(query['enabled'])


def test_post_anything(api_service: AnythingService):
    input_data: AnythingDto = AnythingGenerator.generate()
    response = api_service.post_anything(input_data)
    assert response.status() == 200
    json_data: AnythingDto = AnythingDto(**json.loads(response.json()['data']))
    assert json_data.key_string == input_data.key_string
    assert json_data.key_boolean == input_data.key_boolean
    assert json_data.key_number == input_data.key_number
    assert json_data.key_array_string == input_data.key_array_string
    assert json_data.key_array_obj == input_data.key_array_obj


def test_put_anything(api_service: AnythingService):
    input_data: AnythingDto = AnythingGenerator.generate()
    id_ = 100000
    response = api_service.put_anything(id_, input_data)
    assert response.status() == 200
    json_output = response.json()
    json_data: AnythingDto = AnythingDto(**json.loads(json_output['data']))
    assert json_data.key_string == input_data.key_string
    assert json_data.key_boolean == input_data.key_boolean
    assert json_data.key_number == input_data.key_number
    assert json_data.key_array_string == input_data.key_array_string
    assert json_data.key_array_obj == input_data.key_array_obj
    assert json_output['headers']['Id'] == str(id_)


def test_delete_anything(api_service: AnythingService):
    ids = [10000, 999912, 234234]
    response = api_service.delete_anything(ids)
    assert response.status() == 200
    json_data = json.loads(response.json()['data'])
    assert json_data['ids'] == ids
