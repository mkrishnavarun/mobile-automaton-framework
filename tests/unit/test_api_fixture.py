from unittest.mock import patch

from api.api_client import APIClient
from config.config_loader import ConfigLoader


def test_api_client_fixture_initialization(api_client):
    assert isinstance(api_client, APIClient)
    assert api_client.base_url == "https://jsonplaceholder.typicode.com"
    assert api_client.timeout == 10


def test_api_client_closes_session():
    config = ConfigLoader("local")

    with patch("tests.conftest.APIClient") as mock_api_client:
        client = mock_api_client.return_value

        from tests.conftest import api_client as fixture_function

        generator = fixture_function.__wrapped__(config)

        yielded_client = next(generator)

        assert yielded_client is client

        try:
            next(generator)
        except StopIteration:
            pass

        client.close.assert_called_once()