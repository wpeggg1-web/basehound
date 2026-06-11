"""
Skill: Token Analysis
Sources: GoPlus Security API + Basescan API
Chain: Base (chain_id = 8453)
"""

import requests
from config.settings import settings

BASE_CHAIN_ID = "8453"
GOPLUS_URL = "https://api.gopluslabs.io/api/v1/token_security/" + BASE_CHAIN_ID
BASESCAN_URL = "https://api.basescan.org/api"


def analyze_token(address: str) -> str:
    goplus_data = _goplus_scan(address)
    basescan_data = _basescan_info(address)
    return _format_report(address, goplus_data, basescan_data)


def _goplus_scan(address: str) -> dict:
    try:
        params = {"contract_addresses": address}
        headers = {}
        if settings.GOPLUS_API_KEY:
            headers["Authorization"] = settings.GOPLUS_API_KEY
        r = requests.get(GOPLUS_URL, params=params, headers=headers, timeout=10)
        data = r.json()
        if data.get("code") == 1 and data.get("result"):
            return data["result"].get(address.lower(), {})
    except Exception as e:
        return {"error": str(e)}
    return {}


def _basescan_info(address: str) -> dict:
    try:
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": address,
            "apikey": settings.BASESCAN_API_KEY or "YourApiKeyToken"
        }
        r = requests.get(BASESCAN_URL, params=params, timeout=10)
        data = r.json()
        if data.get("status") == "1" and data.get("result"):
            return data["result"][0]
    except Exception as e:
        return {"error": str(e)}
    return {}


def _fmt_flag(val, label: str, safe_val="1") -> str:
    if val == safe_val:
        return f"✅ {label}"
    elif val == "0":
        return f"🚨 {label}"
    return f"❓ {label} (unknown)"


def _format_report(address: str, gp: dict, bs: dict) -> str:
    if not gp and not bs:
        return f"⚠️ No data found for `{address}` on Base."

    lines = [f"🐾 *Token Analysis*\n`{address}`\n"]

    # GoPlus
    if gp and "error" not in gp:
        lines.append("*🔒 Security (GoPlus)*")
        lines.append(_fmt_flag(gp.get("is_honeypot"), "Not a honeypot"))
        lines.append(_fmt_flag(gp.get("owner_change_balance"), "Owner cannot change balance", safe_val="0"))
        lines.append(_fmt_flag(gp.get("cannot_sell_all"), "Can sell all tokens", safe_val="0"))
        lines.append(_fmt_flag(gp.get("is_mintable"), "Not mintable", safe_val="0"))
        lines.append(_fmt_flag(gp.get("owner_address", "0x000") == "0x0000000000000000000000000000000000000000" or gp.get("renounced") == "1", "Ownership renounced"))

        buy_tax = gp.get("buy_tax", "?")
        sell_tax = gp.get("sell_tax", "?")
        lines.append(f"\n💰 Buy tax: `{buy_tax}` | Sell tax: `{sell_tax}`")

        holders = gp.get("holder_count", "?")
        lines.append(f"👥 Holders: `{holders}`")

        lp_locked = gp.get("lp_locked_percent", None)
        if lp_locked:
            lines.append(f"🔐 LP locked: `{lp_locked}%`")

        top_holders = gp.get("holders", [])
        if top_holders:
            lines.append("\n*Top holders:*")
            for h in top_holders[:3]:
                pct = float(h.get("percent", 0)) * 100
                tag = h.get("tag", h.get("address", "")[:10] + "...")
                lines.append(f"  • {tag}: `{pct:.2f}%`")
    else:
        lines.append("⚠️ GoPlus data unavailable")

    # Basescan
    lines.append("\n*📄 Contract (Basescan)*")
    if bs and "error" not in bs:
        verified = bs.get("ABI", "") != "Contract source code not verified"
        lines.append(f"{'✅' if verified else '🚨'} Source {'verified' if verified else 'NOT verified'}")
        name = bs.get("ContractName", "Unknown")
        lines.append(f"📛 Name: `{name}`")
        compiler = bs.get("CompilerVersion", "?")
        lines.append(f"🛠 Compiler: `{compiler}`")
    else:
        lines.append("⚠️ Basescan data unavailable")

    lines.append(f"\n🔗 [View on Basescan](https://basescan.org/token/{address})")
    return "\n".join(lines)
