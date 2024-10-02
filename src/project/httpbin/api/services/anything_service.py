import logging

from core.api.base_api_service import BaseApiService
from core.api.request_options import RequestOptions
from core.api.response import Response
from project.httpbin.utils.data.anything_dto import AnythingDto

log = logging.getLogger()


class AnythingService(BaseApiService):
    resources = {
        'get': '/anything',
        'post': '/anything',
        'put': '/anything',
        'delete': '/anything',
    }

    def get_anything(self, query: dict) -> Response:
        log.info('Get anything')
        return self.http_client.get(self.resources['get'], RequestOptions(params=query))

    def post_anything(self, data: AnythingDto):
        log.info('Post anything')
        return self.http_client.post(self.resources['post'], RequestOptions(data=vars(data)))

    def put_anything(self, id_: int, data: AnythingDto):
        log.info('Put anything')
        return self.http_client.put(self.resources['put'], RequestOptions(data=vars(data), headers={'id': str(id_)}))

    def delete_anything(self, ids: list[int]):
        log.info('Delete anything')
        return self.http_client.delete(self.resources['delete'], RequestOptions(data={'ids': ids}))
