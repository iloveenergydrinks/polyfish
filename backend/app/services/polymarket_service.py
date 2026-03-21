"""
Polymarket market metadata service.

Read-only access to Polymarket's public Gamma API for active-market metadata.
"""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
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
        normalized_slug = self._normalize_lookup_slug(slug)

        if market_id:
            markets = self._get_json("/markets", {"id": market_id})
        elif normalized_slug:
            markets = self._get_json("/markets", {"slug": normalized_slug})
            if not markets:
                markets = self._get_market_from_event_slug(normalized_slug)
            if not markets:
                markets = self._find_market_by_fuzzy_slug(normalized_slug)
        else:
            raise ValueError("market_id or slug is required")

        if not markets:
            raise ValueError("Market not found on Polymarket")

        return self._normalize_market(markets[0])

    def _get_market_from_event_slug(self, slug: str) -> List[Dict[str, Any]]:
        events = self._get_json("/events", {"slug": slug})
        if not events:
            return []

        event = events[0] or {}
        event_markets = event.get("markets") or []
        if not event_markets:
            return []

        exact_slug_match = [market for market in event_markets if (market or {}).get("slug") == slug]
        if exact_slug_match:
            return exact_slug_match

        active_markets = [market for market in event_markets if (market or {}).get("active")]
        return active_markets or event_markets[:1]

    def _find_market_by_fuzzy_slug(self, slug: str) -> List[Dict[str, Any]]:
        query_key = self._canonicalize_lookup_text(slug)
        if not query_key:
            return []

        best_market: Optional[Dict[str, Any]] = None
        best_score = 0.0

        for offset in range(0, 1000, 500):
            candidates = self._get_json(
                "/markets",
                {
                    "active": "true",
                    "closed": "false",
                    "limit": 500,
                    "offset": offset,
                },
            )
            if not candidates:
                break

            for market in candidates:
                score = self._score_market_candidate(query_key, market or {})
                if score > best_score:
                    best_market = market
                    best_score = score

            if best_score >= 0.995 or len(candidates) < 500:
                break

        return [best_market] if best_market and best_score >= 0.9 else []

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

    @staticmethod
    def _normalize_lookup_slug(value: Optional[str]) -> Optional[str]:
        if not value:
            return None

        raw = str(value).strip()
        if not raw:
            return None

        if raw.startswith("http://") or raw.startswith("https://"):
            try:
                parsed = urlparse(raw)
                path_parts = [part for part in parsed.path.split("/") if part]
                return path_parts[-1] if path_parts else None
            except ValueError:
                return raw

        path_parts = [part for part in raw.strip("/").split("/") if part]
        return path_parts[-1] if path_parts else raw.strip("/")

    @classmethod
    def _canonicalize_lookup_text(cls, value: Optional[str]) -> str:
        raw = cls._normalize_lookup_slug(value) or ""
        if not raw:
            return ""

        raw = re.sub(r"(?:-\d+)+$", "", raw.lower())
        for phrase in ("greater-than", "less-than", "greater than", "less than"):
            raw = raw.replace(phrase, " ")
        raw = raw.replace(">", " ").replace("<", " ")
        raw = re.sub(r"[^a-z0-9]+", " ", raw)
        return " ".join(raw.split())

    @classmethod
    def _score_market_candidate(cls, query_key: str, market: Dict[str, Any]) -> float:
        slug_key = cls._canonicalize_lookup_text(market.get("slug"))
        question_key = cls._canonicalize_lookup_text(market.get("question"))

        candidate_keys = [key for key in (slug_key, question_key) if key]
        if not candidate_keys:
            return 0.0

        best_ratio = max(SequenceMatcher(None, query_key, key).ratio() for key in candidate_keys)

        if any(key == query_key for key in candidate_keys):
            return 1.0

        if any(key.startswith(query_key) or query_key.startswith(key) for key in candidate_keys):
            best_ratio = max(best_ratio, 0.98)

        query_tokens = set(query_key.split())
        if query_tokens:
            best_overlap = 0.0
            for key in candidate_keys:
                candidate_tokens = set(key.split())
                if not candidate_tokens:
                    continue
                overlap = len(query_tokens & candidate_tokens) / max(len(query_tokens), len(candidate_tokens))
                best_overlap = max(best_overlap, overlap)
            best_ratio = max(best_ratio, best_overlap)

        return best_ratio
