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
        self.login_card_number = -1
        self.bot.add_handler(CommandHandler(bot_messages.START_CMD, self.start))
        self.bot.add_handler(CommandHandler(bot_messages.REGISTER_CMD, self.register))
        self.bot.add_handler(CommandHandler(bot_messages.LOGIN_CMD, self.login))
        self.bot.add_handler(CommandHandler(bot_messages.QUIT_CMD, self.quit))
        # self.bot.add_handler(CommandHandler(bot_messages.TRANSFER_CMD, self.transfer))

    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.args
        if len(user_data) == 4:
            if not self.db.is_user_exists(user_data[1], user_data[0], user_data[2]):
                self.db.save_user(user_data=user_data)
                await update.message.reply_text(bot_messages.set_service_success_msg(user_data[1]))
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.ALREADY_EXISTS_USER_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.INCORRECT_INPUT_MSG)

    async def login(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.args
        if len(user_data) == 2:
            if self.login_card_number != -1:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.ALREADY_LOGIN_USER_MSG)
            # await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.SUCCESS_LOGIN_MSG)
            elif self.db.login_user(user_data[1], int(user_data[0])):
                self.login_card_number = int(user_data[0])
                await update.message.reply_text(bot_messages.set_login_success_msg(int(user_data[0])))
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGINING_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGIN_INPUT_MSG)

    async def quit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.login_card_number != -1:
            self.login_card_number = -1
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.QUIT_SUCCESSFUL_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_ALREADY_LOGING_MSG)

    async def transfer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        transfer_data = context.args
        if self.login_card_number == -1:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_ALREADY_LOGING_MSG)
        elif len(transfer_data) == 2:
            self.db.change_balance(self.login_card_number, transfer_data[1])
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.TRANSFER_SUCCESSFUL_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.TRANSFER_INPUT_ERROR_MSG)

    @staticmethod
    async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(bot_messages.HELLO_MSG)

