"""
BASEHOUND Agent Core — Hermes Agent Framework integration
"""

import re
from skills.token_analysis import analyze_token
from skills.defi_alpha import get_alpha
from skills.wallet_intel import get_wallet_intel
from config.settings import settings


SYSTEM_PROMPT = """You are BASEHOUND, a blunt and sharp Base ecosystem intelligence agent.
You hunt DeFi alpha, analyze tokens for rugs, and profile wallets like a pro.
- Keep responses short and direct. No fluff.
- Use data to back every claim.
- If something looks like a rug, say it.
- You live on Base. You breathe Base.
"""


class BasehoundAgent:
    def __init__(self):
        self.history = []
        self._init_llm()

    def _init_llm(self):
        """Initialize LLM via configured provider"""
        provider = settings.LLM_PROVIDER.lower()
        if provider == "openrouter":
            import openai
            self.client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=settings.LLM_API_KEY
            )
        elif provider == "groq":
            import openai
            self.client = openai.OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=settings.LLM_API_KEY
            )
        else:
            # Pioneer / freemodel or OpenAI-compatible default
            import openai
            self.client = openai.OpenAI(
                base_url=settings.LLM_BASE_URL,
                api_key=settings.LLM_API_KEY or "none"
            )

    def process(self, user_input: str, context: dict = None) -> str:
        """Main processing — route to skill or LLM"""
        lower = user_input.lower()

        # Skill routing by keyword / command pattern
        addr_match = re.search(r"0x[a-fA-F0-9]{40}", user_input)

        if addr_match and any(kw in lower for kw in ["analyze", "token", "check", "scan", "rug"]):
            return analyze_token(addr_match.group())

        if addr_match and any(kw in lower for kw in ["wallet", "address", "portfolio", "pnl", "holdings"]):
            return get_wallet_intel(addr_match.group())

        if any(kw in lower for kw in ["alpha", "trending", "hot", "movers", "new pool", "gem"]):
            return get_alpha()

        # Fallback to LLM
        return self._llm_chat(user_input)

    def _llm_chat(self, user_input: str) -> str:
        self.history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.history[-10:]
        try:
            resp = self.client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                max_tokens=512
            )
            reply = resp.choices[0].message.content
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"⚠️ LLM error: {e}"

    # ─── Telegram command handlers ───────────────────────────────────────────

    async def cmd_start(self, update, context):
        await update.message.reply_text(
            "🐾 *BASEHOUND online.*\n\n"
            "I hunt alpha, scan tokens, and profile wallets on Base.\n\n"
            "Commands:\n"
            "/analyze `<token_address>` — security scan\n"
            "/wallet `<wallet_address>` — wallet intel\n"
            "/alpha — trending tokens on Base\n"
            "/help — full command list",
            parse_mode="Markdown"
        )

    async def cmd_analyze(self, update, context):
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /analyze <token_address>")
            return
        addr = args[0]
        if not re.match(r"0x[a-fA-F0-9]{40}", addr):
            await update.message.reply_text("❌ Invalid address format.")
            return
        await update.message.reply_text("🔍 Scanning token...")
        result = analyze_token(addr)
        await update.message.reply_text(result, parse_mode="Markdown")

    async def cmd_wallet(self, update, context):
        args = context.args
        if not args:
            await update.message.reply_text("Usage: /wallet <wallet_address>")
            return
        addr = args[0]
        if not re.match(r"0x[a-fA-F0-9]{40}", addr):
            await update.message.reply_text("❌ Invalid address format.")
            return
        await update.message.reply_text("🕵️ Profiling wallet...")
        result = get_wallet_intel(addr)
        await update.message.reply_text(result, parse_mode="Markdown")

    async def cmd_alpha(self, update, context):
        await update.message.reply_text("📈 Hunting alpha...")
        result = get_alpha()
        await update.message.reply_text(result, parse_mode="Markdown")

    async def cmd_help(self, update, context):
        await update.message.reply_text(
            "🐾 *BASEHOUND Commands*\n\n"
            "/analyze `<address>` — Token security scan (GoPlus + Basescan)\n"
            "/wallet `<address>` — Wallet portfolio + swap history\n"
            "/alpha — Trending tokens + new pools on Base\n"
            "/start — Introduction\n\n"
            "You can also just chat naturally — I understand context.",
            parse_mode="Markdown"
        )

    async def cmd_chat(self, update, context):
        user_input = update.message.text
        response = self.process(user_input)
        await update.message.reply_text(response, parse_mode="Markdown")
