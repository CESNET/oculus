import threading
from datetime import datetime, timedelta
from typing import Optional
import httpx

import logging


class TokenManager:
    """
    Thread-safe token manager for OAuth2 authentication.
    Handles token acquisition and automatic refresh when expired or nearly expired.
    """

    def __init__(
            self,
            token_url: str,
            username: str,
            password: str,
            client_id: str,
            client_secret: Optional[str] = None,
            refresh_threshold_seconds: int = 300
    ):
        """
        Initialize the GSS token manager.

        Args:
            token_url: OAuth2 token endpoint URL
            username: Username for authentication
            password: Password for authentication
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret (optional)
            refresh_threshold_seconds: Refresh token this many seconds before expiry (default: 300)
        """
        self._token_url = token_url
        self._username = username
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret
        self._refresh_threshold = refresh_threshold_seconds

        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None
        self._lock = threading.Lock()
        self._logger = logging.getLogger(__name__)

    def _request_token(self) -> dict:
        """
        Request a new access token from the token endpoint.

        Returns:
            dict: Token response containing access_token, expires_in, etc.

        Raises:
            httpx.HTTPError: If token request fails
        """
        data = {
            "grant_type": "password",
            "username": self._username,
            "password": self._password,
            "client_id": self._client_id,
        }

        if self._client_secret:
            data["client_secret"] = self._client_secret

        self._logger.debug(f"Requesting token from {self._token_url}")
        with httpx.Client() as client:
            response = client.post(self._token_url, data=data)
            response.raise_for_status()
            return response.json()

    def _is_token_expired(self) -> bool:
        """
        Check if the current token is expired or nearly expired.

        Returns:
            bool: True if token is None, expired, or nearly expired
        """
        if self._access_token is None or self._token_expiry is None:
            self._logger.debug(f"Token for client {self._client_id} is expired or never acquired.")
            return True

        threshold_time = datetime.now() + timedelta(seconds=self._refresh_threshold)
        return threshold_time >= self._token_expiry

    def get_token(self) -> str:
        """
        Get a valid access token, refreshing if necessary.
        This method is thread-safe.

        Returns:
            str: Valid access token

        Raises:
            httpx.HTTPError: If token request fails
        """
        with self._lock:
            if self._is_token_expired():
                token_response = self._request_token()
                self._access_token = token_response["access_token"]
                expires_in = token_response.get("expires_in", 3600)
                self._token_expiry = datetime.now() + timedelta(seconds=expires_in)

            return self._access_token
