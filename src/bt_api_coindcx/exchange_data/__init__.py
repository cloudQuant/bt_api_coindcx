from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData

_FALLBACK_REST_PATHS = {
    "get_server_time": "GET /exchange/v1/time",
    "get_exchange_info": "GET /exchange/v1/markets_details",
    "get_tick": "GET /exchange/ticker",
    "get_depth": "GET /exchange/v1/orderbook/",
    "get_kline": "GET /market_data/candles",
    "get_trades": "GET /exchange/v1/trades",
    "make_order": "POST /exchange/v1/orders/create",
    "cancel_order": "POST /exchange/v1/orders/cancel",
    "query_order": "POST /exchange/v1/orders/status",
    "get_open_orders": "POST /exchange/v1/orders/active_orders",
    "get_balance": "POST /exchange/v1/users/balances",
    "get_account": "POST /exchange/v1/users/info",
}


class CoinDCXExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "coindcx"
        self.rest_url = "https://api.coindcx.com"
        self.wss_url = "wss://stream.coindcx.com"
        self.rest_paths = dict(_FALLBACK_REST_PATHS)
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "4h": "4h",
            "1d": "1d",
            "1w": "1w",
        }
        self.legal_currency = ["INR", "USDT", "BTC", "ETH"]

    def get_symbol(self, symbol: str) -> str:
        return symbol.upper().replace("/", "").replace("-", "").replace("_", "")

    def get_period(self, key: str) -> str:
        return self.kline_periods.get(key, key)

    def get_rest_path(self, key: str, **kwargs) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            raise ValueError(f"[{self.exchange_name}] REST path not found: {key}")
        return self.rest_paths[key]


class CoinDCXExchangeDataSpot(CoinDCXExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"
        self.api_key: str | None = None
        self.api_secret: str | None = None
