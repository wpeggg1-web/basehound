"""
Skill: DeFi Alpha
Sources: GeckoTerminal API + Dexscreener API
Chain: Base
"""

import requests

GECKO_BASE_URL = "https://api.geckoterminal.com/api/v2"
DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/tokens"


def get_alpha() -> str:
    trending = _gecko_trending()
    new_pools = _gecko_new_pools()
    return _format_alpha(trending, new_pools)


def _gecko_trending() -> list:
    """Top tokens by 24h volume on Base"""
    try:
        r = requests.get(
            f"{GECKO_BASE_URL}/networks/base/tokens",
            params={"sort": "h24_volume_usd_desc", "page": 1},
            headers={"Accept": "application/json"},
            timeout=10
        )
        data = r.json()
        return data.get("data", [])[:6]
    except Exception:
        return []


def _gecko_new_pools() -> list:
    """Newest pools on Base with decent liquidity"""
    try:
        r = requests.get(
            f"{GECKO_BASE_URL}/networks/base/new_pools",
            params={"page": 1},
            headers={"Accept": "application/json"},
            timeout=10
        )
        data = r.json()
        pools = data.get("data", [])
        # filter pools with > $10k reserve
        filtered = []
        for p in pools:
            attrs = p.get("attributes", {})
            reserve = float(attrs.get("reserve_in_usd", 0) or 0)
            if reserve >= 10000:
                filtered.append(p)
        return filtered[:5]
    except Exception:
        return []


def _fmt_usd(val) -> str:
    try:
        v = float(val)
        if v >= 1_000_000:
            return f"${v/1_000_000:.2f}M"
        if v >= 1_000:
            return f"${v/1_000:.1f}K"
        return f"${v:.2f}"
    except Exception:
        return "$?"


def _format_alpha(trending: list, new_pools: list) -> str:
    lines = ["📈 *Base DeFi Alpha*\n"]

    # Trending tokens
    lines.append("*🔥 Top Volume (24h)*")
    if trending:
        for t in trending:
            attrs = t.get("attributes", {})
            name = attrs.get("name", "?")
            symbol = attrs.get("symbol", "?")
            price = attrs.get("price_usd", "?")
            vol = _fmt_usd(attrs.get("volume_usd", {}).get("h24", 0))
            change = attrs.get("price_change_percentage", {}).get("h24", "?")
            try:
                change_str = f"{float(change):+.1f}%"
                emoji = "🟢" if float(change) >= 0 else "🔴"
            except Exception:
                change_str, emoji = "?", "⚪"
            lines.append(f"{emoji} *{symbol}* ({name}) | ${price} | Vol: {vol} | {change_str}")
    else:
        lines.append("⚠️ Couldn't fetch trending data")

    # New pools
    lines.append("\n*🆕 New Pools (>$10K liquidity)*")
    if new_pools:
        for p in new_pools:
            attrs = p.get("attributes", {})
            name = attrs.get("name", "?")
            reserve = _fmt_usd(attrs.get("reserve_in_usd", 0))
            vol = _fmt_usd(attrs.get("volume_usd", {}).get("h24", 0))
            created = attrs.get("pool_created_at", "")[:10]
            lines.append(f"🌊 *{name}* | Liq: {reserve} | Vol 24h: {vol} | Created: {created}")
    else:
        lines.append("⚠️ No new pools with >$10K liquidity found")

    lines.append(f"\n🔗 [More on GeckoTerminal](https://www.geckoterminal.com/base/pools)")
    return "\n".join(lines)
