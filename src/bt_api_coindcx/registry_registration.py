from __future__ import annotations

from bt_api_base.registry import ExchangeRegistry

from bt_api_coindcx.exchange_data import CoinDCXExchangeDataSpot
from bt_api_coindcx.feeds.live_coindcx.spot import CoinDCXRequestDataSpot


def register_coindcx(registry: ExchangeRegistry | type[ExchangeRegistry]) -> None:
    registry.register_feed("COINDCX___SPOT", CoinDCXRequestDataSpot)
    registry.register_exchange_data("COINDCX___SPOT", CoinDCXExchangeDataSpot)


def register(registry: ExchangeRegistry | None = None) -> None:
    if registry is None:
        register_coindcx(ExchangeRegistry)
        return
    register_coindcx(registry)
