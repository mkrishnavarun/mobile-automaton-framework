from unittest.mock import MagicMock, patch

from api.api_client import APIClient
import requests


def test_get_request():
    client = APIClient("https://example.com")

    with patch.object(client.session, "get") as mock_get:
        mock_get.return_value = MagicMock(status_code=200)

        response = client.get("/users")

        mock_get.assert_called_once_with(
            "https://example.com/users",
            timeout=10,
        )
        assert response.status_code == 200

    client.close()


def test_post_request():
    client = APIClient("https://example.com")

    with patch.object(client.session, "post") as mock_post:
        mock_post.return_value = MagicMock(status_code=201)

        response = client.post(
            "/users",
            {"name": "Varun"},
        )

        mock_post.assert_called_once_with(
            "https://example.com/users",
            json={"name": "Varun"},
            timeout=10,
        )
        assert response.status_code == 201

    client.close()


def test_put_request():
    client = APIClient("https://example.com")

    with patch.object(client.session, "put") as mock_put:
        mock_put.return_value = MagicMock(status_code=200)

        response = client.put(
            "/users/1",
            {"name": "Updated User"},
        )

        mock_put.assert_called_once_with(
            "https://example.com/users/1",
            json={"name": "Updated User"},
            timeout=10,
        )
        assert response.status_code == 200

    client.close()


def test_delete_request():
    client = APIClient("https://example.com")

    with patch.object(client.session, "delete") as mock_delete:
        mock_delete.return_value = MagicMock(status_code=204)

        response = client.delete("/users/1")

        mock_delete.assert_called_once_with(
            "https://example.com/users/1",
            timeout=10,
        )
        assert response.status_code == 204

    client.close()


def test_base_url_trailing_slash():
    client = APIClient("https://example.com/")

    assert client.base_url == "https://example.com"

    client.close()


def test_get_request_timeout():
    client = APIClient("https://example.com", timeout=1)

    try:
        with patch.object(
            client.session,
            "get",
            side_effect=requests.exceptions.Timeout,
        ) as mock_get:

            try:
                client.get("/users")
                assert False, "Expected a timeout exception"
            except requests.exceptions.Timeout:
                pass

            mock_get.assert_called_once_with(
                "https://example.com/users",
                timeout=1,
            )
    finally:
        client.close()


def test_get_request_returns_http_error_response():
    client = APIClient("https://example.com")

    try:
        with patch.object(client.session, "get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=404,
                json=lambda: {"error": "Not found"},
            )

            response = client.get("/users/999")

            assert response.status_code == 404
            assert response.json() == {"error": "Not found"}

            mock_get.assert_called_once_with(
                "https://example.com/users/999",
                timeout=10,
            )
    finally:
        client.close()