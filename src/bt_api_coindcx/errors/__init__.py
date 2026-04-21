from __future__ import annotations

from typing import Any

from bt_api_base.error import ErrorCategory, ErrorTranslator, UnifiedError, UnifiedErrorCode


class CoinDCXErrorTranslator(ErrorTranslator):
    @classmethod
    def translate(cls, raw_error: dict[str, Any], venue: str) -> UnifiedError | None:
        code = raw_error.get("code", raw_error.get("errorCode"))
        message = str(raw_error.get("message", raw_error.get("error", "")))
        message_lower = message.lower()
        if code == 401 or "auth" in message_lower:
            return cls._build_error(UnifiedErrorCode.INVALID_API_KEY, venue, raw_error)
        if code == 429 or "rate" in message_lower:
            return cls._build_error(UnifiedErrorCode.RATE_LIMIT_EXCEEDED, venue, raw_error)
        if "balance" in message_lower or "insufficient" in message_lower:
            return cls._build_error(UnifiedErrorCode.INSUFFICIENT_BALANCE, venue, raw_error)
        if "not found" in message_lower or code == 404:
            return cls._build_error(UnifiedErrorCode.ORDER_NOT_FOUND, venue, raw_error)
        if "invalid" in message_lower or code == 400:
            return cls._build_error(UnifiedErrorCode.INVALID_PARAMETER, venue, raw_error)
        return super().translate(raw_error, venue)

    @staticmethod
    def _build_error(code: UnifiedErrorCode, venue: str, raw_error: dict[str, Any]) -> UnifiedError:
        message = str(raw_error.get("message", raw_error.get("error", code.name)))
        return UnifiedError(
            code=code,
            category=ErrorCategory.BUSINESS,
            venue=venue,
            message=message,
            original_error=str(raw_error),
            context={"raw_response": raw_error},
        )
