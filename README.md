# 🐾 BASEHOUND

> **On-chain intelligence agent for the Base ecosystem — built on Hermes Agent Framework**

BASEHOUND is an AI-powered crypto intelligence agent that hunts DeFi alpha, analyzes tokens, and profiles wallets — all natively on Base. Deploy it as a Telegram bot or CLI tool with zero centralized backend.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Token Analysis** | Security scoring via GoPlus + contract verification via Basescan |
| 📈 **DeFi Alpha** | Trending tokens, new pools, and volume spikes on Base |
| 🕵️ **Wallet Intel** | Wallet profiling — PnL, top holdings, recent swaps |
| ⚡ **Hermes-native** | Runs on Hermes Agent Framework with modular skill slots |
| 🤖 **Telegram Bot** | Full bot interface out of the box |

---

## 🏗️ Architecture

```
BASEHOUND
├── Hermes Agent Framework (LLM core + skill routing)
├── Skills
│   ├── token_analysis   → GoPlus API + Basescan API
│   ├── defi_alpha       → GeckoTerminal + Dexscreener API
│   └── wallet_intel     → Basescan + Zapper API
└── Interface
    └── Telegram Bot (python-telegram-bot)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Hermes Agent Framework installed
- API keys: GoPlus, Basescan, Telegram Bot Token

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/basehound
cd basehound
pip install -r requirements.txt
cp config/.env.example config/.env
# Fill in your API keys in config/.env
python main.py
```

---

## ⚙️ Configuration

```env
# config/.env
TELEGRAM_BOT_TOKEN=your_token_here
BASESCAN_API_KEY=your_key_here
GOPLUS_API_KEY=your_key_here
LLM_PROVIDER=openrouter         # or groq, pioneer
LLM_MODEL=anthropic/claude-3-haiku
AGENT_NAME=BASEHOUND
AGENT_PERSONA=blunt
```

---

## 🛠️ Skills

### `/analyze <token_address>`
Full security scan + contract info:
- GoPlus security score (honeypot, ownership renounced, liquidity locked)
- Basescan contract verification status
- Top holders distribution
- Buy/sell tax

### `/alpha`
Trending tokens on Base right now:
- Top gainers (24h) from GeckoTerminal
- New pools < 24h with liquidity > $10k
- Volume spike alerts

### `/wallet <address>`
Wallet intelligence report:
- Token portfolio + USD value
- Recent swap history
- Estimated PnL (unrealized)
- "Degen score" based on activity

---

## 📁 Project Structure

```
basehound/
├── main.py                  # Entry point
├── agent.py                 # Hermes agent init + routing
├── requirements.txt
├── skills/
│   ├── token_analysis.py    # GoPlus + Basescan
│   ├── defi_alpha.py        # GeckoTerminal + Dexscreener
│   └── wallet_intel.py      # Wallet profiling
├── config/
│   ├── .env.example
│   └── settings.py
├── docs/
│   └── SKILLS.md
└── assets/
    └── logo.png
```

---

## 🔑 API Keys Setup

| Service | Free Tier | Get Key |
|---|---|---|
| Basescan | ✅ 5 req/s | [basescan.org/apis](https://basescan.org/apis) |
| GoPlus | ✅ Limited | [gopluslabs.io](https://gopluslabs.io) |
| GeckoTerminal | ✅ No key needed | Public API |
| Dexscreener | ✅ No key needed | Public API |
| OpenRouter | ✅ Free credits | [openrouter.ai](https://openrouter.ai) |

---

## 📜 License

MIT — free to fork, build, deploy.

---

## 🤝 Built on

- [Hermes Agent Framework](https://github.com/hermesagent)
- [GoPlus Security API](https://gopluslabs.io)
- [Basescan API](https://basescan.org/apis)
- [GeckoTerminal API](https://api.geckoterminal.com)
- [Dexscreener API](https://dexscreener.com)
