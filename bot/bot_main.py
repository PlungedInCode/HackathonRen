import os

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from sqlalchemy.orm import sessionmaker
from bot import bot_messages
from db.db_api import Database

from db.models import User


class Bot:
    def __init__(self, db: Database):
        self.db = db
        self.bot = Application.builder() \
            .token(os.getenv("BOT_TOKEN")) \
            .build()
        self.bot.add_handler(CommandHandler(bot_messages.START_CMD, self.start))
        self.bot.add_handler(CommandHandler(bot_messages.REGISTER_CMD, self.register))

    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.args
        if len(user_data) == 4:
            if not self.db.is_user_exists(user_data[1], user_data[0], user_data[2]):
                self.db.save_user(user_data=user_data)
                await update.message.reply_text(bot_messages.set_service_success_msg(user_data[1]))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.INCORRECT_INPUT_MSG)

    @staticmethod
    async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(bot_messages.HELLO_MSG)

