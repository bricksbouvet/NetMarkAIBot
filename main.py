import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

# ---- Edit these if you want different wording -------------------------------
URL = "https://www.netmark.ai/super"
BOT_NAME = "Beyond The Game"
BUTTON_TEXT = "🔗 Visit the Link"

WELCOME = (
    f"⚽ Welcome to {BOT_NAME}!\n\n"
    "Millions of football fans follow the world's biggest tournaments. "
    "But watching is only one way to engage with the game.\n\n"
    "Curious to discover another way to get involved?\n\n"
    "🎬 Tap the button below to watch the free introductory video.\n\n"
    "ℹ️ Independent affiliate promotion. No income is promised."
)
# -----------------------------------------------------------------------------

KEYBOARD = InlineKeyboardMarkup([[InlineKeyboardButton(BUTTON_TEXT, url=URL)]])

# httpx logs request URLs, which contain the bot token, so keep it quiet.
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Works the same for new and returning users."""
    if update.effective_message:
        await update.effective_message.reply_text(WELCOME, reply_markup=KEYBOARD)


def main() -> None:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise SystemExit("BOT_TOKEN is missing. Put it in the .env file.")

    app = Application.builder().token(token).build()
    private = filters.ChatType.PRIVATE
    app.add_handler(CommandHandler("start", start, filters=private))
    # Any other message gets the same welcome + button, so the bot is never silent.
    app.add_handler(MessageHandler(private & (filters.TEXT | filters.COMMAND), start))
    app.run_polling(allowed_updates=[Update.MESSAGE])


if __name__ == "__main__":
    main()
