from django.test import TestCase
from rest_framework.test import APIRequestFactory

from bootcamp.factories import UserFactory


class TestsApiUsers(TestCase):

    request_factory: APIRequestFactory

    def setUp(self):
        self.user1 = UserFactory()
        self.request_factory = APIRequestFactory()

    def test_automatic_user_get_list_endpoint(self):
        client_response = self.client.get('/api/users/')
        factory_response = self.request_factory.get('/api/users/')

        client_json = client_response.json()
        self.assertEquals(client_response.status_code, 200)
        # TODO: fix this
        self.assertGreater(len(client_json), 0)
        # client_json seems to come sorted with the last factory-created user first
        # url indexes seem to start at 1 and username & email suffix at 0
        # self.assertEquals(len(client_json), 2)

        # self.assertEquals(client_json[0]['email'], self.user1_email)
        # self.assertEquals(client_json[0]['groups'], self.user1_groups)

        # TODO: comes back empty (?)
        # print(factory_response.body)
