import os

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler

from bot import bot_messages
from db.db_api import Database


class Bot:
    def __init__(self, db: Database):
        self.db = db
        self.bot = Application.builder()\
            .token(os.getenv("BOT_TOKEN"))\
            .build()
        self.bot.add_handler(CommandHandler(bot_messages.START_CMD, self.start))

    # Пишем тут обработчики команд бота

    @staticmethod
    async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(bot_messages.HELLO_MSG)

