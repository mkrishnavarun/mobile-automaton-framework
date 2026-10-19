import requests


class APIClient:
    """Reusable HTTP client for API testing."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get(self, endpoint: str):
        """Send a GET request."""
        return self.session.get(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            timeout=self.timeout,
        )

    def post(self, endpoint: str, data: dict):
        """Send a POST request."""
        return self.session.post(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            json=data,
            timeout=self.timeout,
        )

    def put(self, endpoint: str, data: dict):
        """Send a PUT request."""
        return self.session.put(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            json=data,
            timeout=self.timeout,
        )

    def delete(self, endpoint: str):
        """Send a DELETE request."""
        return self.session.delete(
            f"{self.base_url}/{endpoint.lstrip('/')}",
            timeout=self.timeout,
        )

    def close(self):
        """Close the HTTP session."""
        self.session.close()