import json

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from app.config import BOT_TOKEN, BASE_URL
from app.agent import ask_gemini
from app.logger import log_interaction

# Store last ~20 messages for each chat
chat_history = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    question = update.message.text

    history = chat_history.setdefault(chat_id, [])

    history.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # Keep last 20 messages
    history = history[-20:]
    chat_history[chat_id] = history

    log_url = f"{BASE_URL}/run.jsonl"

    try:
        response = ask_gemini(history, log_url)

    except Exception as e:
        response = {
            "answer": "internal error",
            "log_url": log_url,
        }

    history.append(
        {
            "role": "assistant",
            "content": json.dumps(response),
        }
    )

    history = history[-20:]
    chat_history[chat_id] = history

    log_interaction(
    question=question,
    response=response,
)

    await update.message.reply_text(
        json.dumps(response, separators=(",", ":"))
    )


def create_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    return app