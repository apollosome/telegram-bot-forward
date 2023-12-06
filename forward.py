#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN_ENV")

destination_group_chat_id = os.getenv("destination_group_chat_id_ENV")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def forward_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await context.bot.sendDocument(chat_id = destination_group_chat_id, caption = 'image caption', document = update.message.document)
        await update.message.reply_text("File forwarded successfully!")
    except Exception as e:
        await update.message.reply_text(f"Failed to forward file: {e} chat id: {update.message.chat_id} file id: {update.message.message_id}")

async def forward_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    # await update.message.reply_text(update.message.message_id)
    # await context.bot.send_message(chat_id=destination_group_chat_id , text=f"Received message: {update.message.text}")
    try:
        await context.bot.forward_message(chat_id=destination_group_chat_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
        await update.message.reply_text("Message forwarded successfully!")
    except Exception as e:
        await update.message.reply_text(f"Failed to forward message: {e} chat id: {update.message.chat_id} message id: {update.message.message_id}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_msg))
    application.add_handler(MessageHandler(filters.Document.ALL, forward_doc))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()