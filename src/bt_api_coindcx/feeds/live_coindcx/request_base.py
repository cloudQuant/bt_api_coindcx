from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient

from bt_api_coindcx.exchange_data import CoinDCXExchangeDataSpot


class CoinDCXRequestData(Feed):
    """CoinDCX REST API Feed base class."""

    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "COINDCX___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = CoinDCXExchangeDataSpot()
        self._params.api_key = (kwargs.get("public_key") or kwargs.get("api_key")) or None
        self._params.api_secret = (
            kwargs.get("private_key") or kwargs.get("secret_key") or kwargs.get("api_secret")
        ) or None
        self.request_logger = self.logger
        self.async_logger = self.logger
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    def _generate_signature(self, body: str = "") -> str:
        """Generate HMAC SHA256 signature for CoinDCX API."""
        secret = self._params.api_secret
        if secret:
            return hmac.new(
                secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
            ).hexdigest()
        return ""

    def _get_headers(self, body: str = "") -> dict[str, str]:
        """Generate request headers."""
        headers = {
            "Content-Type": "application/json",
            "X-AUTH-APIKEY": self._params.api_key or "",
            "X-AUTH-SIGNATURE": self._generate_signature(body),
        }
        return headers

    def request(self, path: str, params=None, body=None, extra_data=None, timeout=10):
        """HTTP request for CoinDCX API."""
        method = path.split()[0] if " " in path else "GET"
        request_path = path.split()[1] if " " in path else path

        if method == "GET":
            headers = {"Content-Type": "application/json"}
            response = self._http_client.request(
                method=method,
                url=self._params.rest_url + request_path,
                headers=headers,
                params=params,
            )
            return self._process_response(response, extra_data)

        json_body = json.dumps(body, separators=(",", ":")) if body else "{}"
        headers = self._get_headers(json_body)
        response = self._http_client.request(
            method=method,
            url=self._params.rest_url + request_path,
            headers=headers,
            json_data=json.loads(json_body),
        )
        return self._process_response(response, extra_data)

    async def async_request(self, path: str, params=None, body=None, extra_data=None, timeout=5):
        """Async HTTP request for CoinDCX API."""
        method = path.split()[0] if " " in path else "GET"
        request_path = path.split()[1] if " " in path else path

        if method == "GET":
            headers = {"Content-Type": "application/json"}
            response = await self._http_client.async_request(
                method=method,
                url=self._params.rest_url + request_path,
                headers=headers,
                params=params,
            )
            return self._process_response(response, extra_data)

        json_body = json.dumps(body, separators=(",", ":")) if body else "{}"
        headers = self._get_headers(json_body)
        response = await self._http_client.async_request(
            method=method,
            url=self._params.rest_url + request_path,
            headers=headers,
            json_data=json.loads(json_body),
        )
        return self._process_response(response, extra_data)

    def async_callback(self, future):
        """Callback for async requests, push result to data_queue."""
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.error(f"Async callback error: {e}")

    def _process_response(self, response, extra_data=None):
        """Process API response."""
        if extra_data is None:
            extra_data = {}
        return RequestData(response, extra_data)

    def push_data_to_queue(self, data):
        """Push data to the queue."""
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self):
        pass

    def disconnect(self):
        super().disconnect()

    def is_connected(self):
        return True

    def _get_server_time(self, extra_data=None, **kwargs):
        """Prepare server time request."""
        if extra_data is None:
            extra_data = {}
        extra_data.update(
            {
                "exchange_name": self.exchange_name,
                "symbol_name": "",
                "asset_type": self.asset_type,
                "request_type": "get_server_time",
            }
        )
        return "GET /exchange/v1/time", {}, extra_data

    def get_server_time(self, extra_data=None, **kwargs):
        """Get server time."""
        path, params, extra_data = self._get_server_time(extra_data, **kwargs)
        return self.request(path, params=params, extra_data=extra_data)
