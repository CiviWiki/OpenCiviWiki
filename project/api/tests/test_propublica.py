from mock import patch, MagicMock

from rest_framework.test import APITestCase, override_settings

from ..propublica import ProPublicaAPI
from .propublica_responses import PROPUBLICA_CORRECT_RESPONSE


@override_settings(PROPUBLICA_API_KEY="test-token")
class ProPublicaAPITestCase(APITestCase):
    def setUp(self):
        self.api_instance = ProPublicaAPI()

    def test_headers_are_set_correctly(self):
        self.assertDictEqual(
            self.api_instance.auth_headers, {"X-API-Key": "test-token"}
        )

    @patch("api.propublica.requests.get")
    def test_if_search_returns_correct_results(self, get_mock):
        get_mock.return_value = MagicMock(
            json=MagicMock(return_value=PROPUBLICA_CORRECT_RESPONSE)
        )
        query = "query"
        data = self.api_instance.search(query)
        self.assertEqual(data, PROPUBLICA_CORRECT_RESPONSE)
        get_mock.assert_called_once_with(
            self.api_instance.URL.format(query=query),
            headers=self.api_instance.auth_headers,
        )
