"""
BASEHOUND - Base Ecosystem Intelligence Agent
Built on Hermes Agent Framework
"""

import os
import logging
from agent import BasehoundAgent
from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("basehound")


def main():
    log.info("🐾 BASEHOUND starting up...")
    log.info(f"Interface: {settings.INTERFACE}")

    agent = BasehoundAgent()

    if settings.INTERFACE == "telegram":
        from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
        app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", agent.cmd_start))
        app.add_handler(CommandHandler("analyze", agent.cmd_analyze))
        app.add_handler(CommandHandler("alpha", agent.cmd_alpha))
        app.add_handler(CommandHandler("wallet", agent.cmd_wallet))
        app.add_handler(CommandHandler("help", agent.cmd_help))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent.cmd_chat))

        log.info("🤖 Telegram bot polling...")
        app.run_polling()

    elif settings.INTERFACE == "cli":
        log.info("💻 CLI mode. Type 'exit' to quit.\n")
        while True:
            try:
                user_input = input("you > ").strip()
                if user_input.lower() in ("exit", "quit"):
                    break
                response = agent.process(user_input)
                print(f"\nBASEHOUND > {response}\n")
            except KeyboardInterrupt:
                break

    log.info("BASEHOUND shutdown.")


if __name__ == "__main__":
    main()
