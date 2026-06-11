"""
Skill: Wallet Intel
Sources: Basescan API (transactions + token holdings)
Chain: Base (chain_id = 8453)
"""

import requests
from config.settings import settings

BASESCAN_URL = "https://api.basescan.org/api"


def get_wallet_intel(address: str) -> str:
    holdings = _get_token_holdings(address)
    recent_txs = _get_recent_txs(address)
    eth_balance = _get_eth_balance(address)
    return _format_wallet(address, eth_balance, holdings, recent_txs)


def _get_eth_balance(address: str) -> float:
    try:
        r = requests.get(BASESCAN_URL, params={
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": settings.BASESCAN_API_KEY or "YourApiKeyToken"
        }, timeout=10)
        data = r.json()
        if data.get("status") == "1":
            return int(data["result"]) / 1e18
    except Exception:
        pass
    return 0.0


def _get_token_holdings(address: str) -> list:
    try:
        r = requests.get(BASESCAN_URL, params={
            "module": "account",
            "action": "tokentx",
            "address": address,
            "sort": "desc",
            "page": 1,
            "offset": 50,
            "apikey": settings.BASESCAN_API_KEY or "YourApiKeyToken"
        }, timeout=10)
        data = r.json()
        if data.get("status") == "1":
            txs = data["result"]
            # Aggregate unique tokens interacted with
            seen = {}
            for tx in txs:
                sym = tx.get("tokenSymbol", "?")
                name = tx.get("tokenName", "?")
                contract = tx.get("contractAddress", "")
                if contract not in seen:
                    seen[contract] = {"symbol": sym, "name": name, "contract": contract, "txs": 0}
                seen[contract]["txs"] += 1
            return list(seen.values())[:8]
    except Exception:
        pass
    return []


def _get_recent_txs(address: str) -> list:
    try:
        r = requests.get(BASESCAN_URL, params={
            "module": "account",
            "action": "txlist",
            "address": address,
            "sort": "desc",
            "page": 1,
            "offset": 10,
            "apikey": settings.BASESCAN_API_KEY or "YourApiKeyToken"
        }, timeout=10)
        data = r.json()
        if data.get("status") == "1":
            return data["result"][:5]
    except Exception:
        pass
    return []


def _degen_score(eth_bal: float, token_count: int, tx_count: int) -> str:
    score = 0
    if token_count >= 10:
        score += 2
    elif token_count >= 5:
        score += 1
    if tx_count >= 20:
        score += 2
    elif tx_count >= 5:
        score += 1
    if eth_bal < 0.01:
        score += 1  # degen burns ETH on gas
    labels = {0: "🧊 Coldwallet / lurker", 1: "😴 Casual", 2: "👀 Active", 3: "🎲 Degen", 4: "🔥 Full degen", 5: "💀 Absolute degen"}
    return labels.get(min(score, 5), "🎲 Degen")


def _short_addr(addr: str) -> str:
    return f"{addr[:6]}...{addr[-4:]}"


def _format_wallet(address: str, eth_bal: float, holdings: list, txs: list) -> str:
    lines = [f"🕵️ *Wallet Intel*\n`{address}`\n"]

    lines.append(f"💎 ETH Balance: `{eth_bal:.4f} ETH`")

    degen = _degen_score(eth_bal, len(holdings), len(txs))
    lines.append(f"🎯 Degen Score: {degen}\n")

    # Token activity
    lines.append("*🪙 Recent Token Activity*")
    if holdings:
        for h in holdings:
            lines.append(f"  • *{h['symbol']}* ({h['name'][:20]}) — {h['txs']} tx(s)")
            lines.append(f"    `{h['contract']}`")
    else:
        lines.append("  No token activity found")

    # Recent txs
    lines.append("\n*⚡ Last 5 Transactions*")
    if txs:
        for tx in txs:
            val_eth = int(tx.get("value", 0)) / 1e18
            to = _short_addr(tx.get("to", ""))
            method = tx.get("functionName", "transfer")[:20] or "transfer"
            status = "✅" if tx.get("txreceipt_status") == "1" else "❌"
            lines.append(f"  {status} `{method}` → {to} | {val_eth:.4f} ETH")
    else:
        lines.append("  No recent transactions found")

    lines.append(f"\n🔗 [View on Basescan](https://basescan.org/address/{address})")
    return "\n".join(lines)
