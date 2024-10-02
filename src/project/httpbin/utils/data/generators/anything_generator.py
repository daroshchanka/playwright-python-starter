from faker.generator import random

from project.httpbin.utils.data.anything_dto import AnythingDto
from faker import Faker
from faker.providers import internet


class AnythingGenerator:

    @staticmethod
    def generate() -> AnythingDto:
        fake = Faker(locale='en_US')
        fake.add_provider(internet)
        result = AnythingDto()
        result.key_string = fake.ipv4_private()
        result.key_number = random.randint(0, 1000000)
        result.key_boolean = fake.boolean(50)
        result.key_array_string = [
            fake.vin(),
            fake.vin(),
            fake.vin(),
        ]
        result.key_array_obj = [
            {'name': fake.first_name(), 'c': 0, 'd': False},
            {'name': fake.first_name(), 'c': 1, 'd': True},
            {'name': fake.first_name(), 'c': 2, 'd': True},
        ]
        return result
