from unittest import TestCase
from pyhearthis.models import as_query_param
from pyhearthis.hearthis_requests import LoginRequest


class TestModels(TestCase):
    def test_that_as_query_param_returns_expected_value(self):
        r = LoginRequest("test@test.de", "mypassword")
        x = as_query_param(r)

        self.assertEqual(x, "email=test%40test.de&password=mypassword")
