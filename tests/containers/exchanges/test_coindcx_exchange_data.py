"""Tests for CoindcxExchangeData container."""

from __future__ import annotations

from bt_api_coindcx.exchange_data import CoinDCXExchangeData


class TestCoinDCXExchangeData:
    """Tests for CoinDCXExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = CoinDCXExchangeData()

        assert exchange.exchange_name == "coindcx"
