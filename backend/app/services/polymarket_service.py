"""
Polymarket market metadata service.

Read-only access to Polymarket's public Gamma API for active-market metadata.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ..config import Config


class PolymarketService:
    """Small wrapper around Polymarket's public Gamma API."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        self.base_url = (base_url or Config.POLYMARKET_GAMMA_BASE_URL).rstrip("/")
        self.timeout = timeout or Config.POLYMARKET_HTTP_TIMEOUT_SECONDS

    def list_active_markets(self, limit: int = 24, offset: int = 0) -> List[Dict[str, Any]]:
        raw_markets = self._get_json(
            "/markets",
            {
                "active": "true",
                "closed": "false",
                "limit": max(1, min(limit, 100)),
                "offset": max(offset, 0),
            },
        )
        return [self._normalize_market(m) for m in raw_markets]

    def get_market(self, market_id: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
        if market_id:
            markets = self._get_json("/markets", {"id": market_id})
        elif slug:
            markets = self._get_json("/markets", {"slug": slug})
        else:
            raise ValueError("market_id or slug is required")

        if not markets:
            raise ValueError("Market not found on Polymarket")

        return self._normalize_market(markets[0])

    def build_market_seed_text(self, market: Dict[str, Any]) -> str:
        event = market.get("event") or {}
        outcome_lines = []
        for outcome in market.get("outcomes", []):
            name = outcome.get("name", "Unknown")
            price = outcome.get("price")
            if price is None:
                outcome_lines.append(f"- {name}")
                continue
            outcome_lines.append(f"- {name}: {price:.3f}")

        description = market.get("description") or "No market description provided."
        resolution_source = market.get("resolution_source") or "No explicit resolution source provided."

        return (
            "Polymarket active market metadata\n"
            f"Question: {market.get('question', '')}\n"
            f"Market slug: {market.get('slug', '')}\n"
            f"Market URL: {market.get('url', '')}\n"
            f"Active: {market.get('active', False)}\n"
            f"Closed: {market.get('closed', False)}\n"
            f"Accepting orders: {market.get('accepting_orders', False)}\n"
            f"Start date: {market.get('start_date', '')}\n"
            f"End date: {market.get('end_date', '')}\n"
            f"Created at: {market.get('created_at', '')}\n"
            f"Updated at: {market.get('updated_at', '')}\n"
            f"Liquidity: {market.get('liquidity', 0)}\n"
            f"Volume: {market.get('volume', 0)}\n"
            f"24h volume: {market.get('volume_24h', 0)}\n"
            f"Best bid: {market.get('best_bid', 0)}\n"
            f"Best ask: {market.get('best_ask', 0)}\n"
            f"Spread: {market.get('spread', 0)}\n"
            f"Last trade price: {market.get('last_trade_price', 0)}\n"
            f"Resolution source: {resolution_source}\n"
            "\n"
            "Event metadata\n"
            f"Event title: {event.get('title', '')}\n"
            f"Event slug: {event.get('slug', '')}\n"
            f"Event start date: {event.get('start_date', '')}\n"
            f"Event end date: {event.get('end_date', '')}\n"
            f"Event volume: {event.get('volume', 0)}\n"
            f"Event liquidity: {event.get('liquidity', 0)}\n"
            "\n"
            "Outcome prices\n"
            f"{chr(10).join(outcome_lines) if outcome_lines else '- No outcome prices available'}\n"
            "\n"
            "Market description\n"
            f"{description}\n"
        )

    def _get_json(self, path: str, params: Dict[str, Any]) -> Any:
        url = f"{self.base_url}{path}?{urlencode(params)}"
        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "PolyFish/0.1",
            },
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise ValueError(f"Polymarket API returned HTTP {exc.code}") from exc
        except URLError as exc:
            raise ValueError(f"Failed to reach Polymarket API: {exc.reason}") from exc

    def _normalize_market(self, market: Dict[str, Any]) -> Dict[str, Any]:
        outcomes = self._parse_json_list(market.get("outcomes"))
        prices = self._parse_json_list(market.get("outcomePrices"))
        paired_outcomes = []

        for idx, outcome_name in enumerate(outcomes):
            paired_outcomes.append(
                {
                    "name": outcome_name,
                    "price": self._to_float(prices[idx]) if idx < len(prices) else None,
                }
            )

        first_event = (market.get("events") or [None])[0] or {}
        event_slug = first_event.get("slug") or market.get("slug", "")

        return {
            "id": str(market.get("id", "")),
            "slug": market.get("slug", ""),
            "question": market.get("question", ""),
            "description": market.get("description") or first_event.get("description") or "",
            "active": bool(market.get("active", False)),
            "closed": bool(market.get("closed", False)),
            "accepting_orders": bool(market.get("acceptingOrders", False)),
            "start_date": market.get("startDate") or market.get("startDateIso") or "",
            "end_date": market.get("endDate") or market.get("endDateIso") or "",
            "created_at": market.get("createdAt", ""),
            "updated_at": market.get("updatedAt", ""),
            "liquidity": self._to_float(market.get("liquidityNum", market.get("liquidity"))),
            "volume": self._to_float(market.get("volumeNum", market.get("volume"))),
            "volume_24h": self._to_float(market.get("volume24hrClob", market.get("volume24hr"))),
            "best_bid": self._to_float(market.get("bestBid")),
            "best_ask": self._to_float(market.get("bestAsk")),
            "spread": self._to_float(market.get("spread")),
            "last_trade_price": self._to_float(market.get("lastTradePrice")),
            "image": market.get("image") or first_event.get("image") or "",
            "icon": market.get("icon") or first_event.get("icon") or "",
            "resolution_source": market.get("resolutionSource") or first_event.get("resolutionSource") or "",
            "url": f"https://polymarket.com/event/{event_slug}" if event_slug else "",
            "outcomes": paired_outcomes,
            "event": {
                "id": str(first_event.get("id", "")),
                "slug": first_event.get("slug", ""),
                "title": first_event.get("title", ""),
                "start_date": first_event.get("startDate", ""),
                "end_date": first_event.get("endDate", ""),
                "liquidity": self._to_float(first_event.get("liquidity")),
                "volume": self._to_float(first_event.get("volume")),
            },
        }

    @staticmethod
    def _parse_json_list(value: Any) -> List[Any]:
        if isinstance(value, list):
            return value
        if not value:
            return []
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                return []
        return []

    @staticmethod
    def _to_float(value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
