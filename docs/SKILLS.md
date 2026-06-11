# BASEHOUND Skills Reference

## token_analysis

**Trigger:** Any message containing a `0x...` token address + keywords like `analyze`, `scan`, `check`, `rug`

**Sources:**
- GoPlus Security API (`https://api.gopluslabs.io/api/v1/token_security/8453`)
- Basescan API (`https://api.basescan.org/api`)

**Output includes:**
- Honeypot status
- Buy/sell tax
- Ownership renounced status
- LP lock percentage
- Top 3 holders + percentages
- Basescan contract verification
- Direct Basescan link

---

## defi_alpha

**Trigger:** Keywords — `alpha`, `trending`, `hot`, `movers`, `new pool`, `gem`

**Sources:**
- GeckoTerminal API (no key needed)
- Dexscreener API (no key needed)

**Output includes:**
- Top 6 tokens by 24h volume on Base
- Price, 24h change, volume per token
- New pools (<24h) with >$10K liquidity
- Pool name, liquidity, 24h volume, creation date

---

## wallet_intel

**Trigger:** Any message containing a `0x...` address + keywords like `wallet`, `portfolio`, `pnl`, `holdings`

**Sources:**
- Basescan API — token transactions + ETH balance

**Output includes:**
- ETH balance
- Degen Score (0–5 scale based on activity)
- Recent unique tokens interacted with
- Last 5 transactions (method, destination, value, status)
- Direct Basescan link
