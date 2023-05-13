import os

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from sqlalchemy.orm import sessionmaker
from bot import bot_messages
from db.db_api import Database
from bot.stats import generate_stats_by_month

from db.models import User

history = ['Income 25.03.2023 100', 'Income 26.03.2023 200', 'Expense 27.03.2023 150']


class Bot:
    def __init__(self, db: Database):
        self.db = db
        self.logged = False
        self.bot = Application.builder() \
            .token(os.getenv("BOT_TOKEN")) \
            .build()
        self.bot.add_handler(CommandHandler(bot_messages.START_CMD, self.start))
        self.bot.add_handler(CommandHandler(bot_messages.REGISTER_CMD, self.register))
        self.bot.add_handler(CommandHandler(bot_messages.BALANCE_CMD, self.balance))
        self.bot.add_handler(CommandHandler(bot_messages.HISTORY_CMD, self.history))
        self.bot.add_handler(CommandHandler(bot_messages.LOGIN_CMD, self.login))
        self.bot.add_handler(CommandHandler(bot_messages.STATS_CMD, self.stats))

    async def register(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.args
        if len(user_data) == 4:
            if not self.db.is_user_exists(user_data[1], user_data[0], user_data[2]):
                self.db.save_user(user_data=user_data)
                self.logged = True
                await update.message.reply_text(bot_messages.set_service_success_msg(user_data[1]))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.INCORRECT_INPUT_MSG)


    async def login(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.args
        print(1)
        if len(user_data) == 2:
            if self.logged:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.ALREADY_LOGIN_USER_MSG)
            # await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.SUCCESS_LOGIN)
            elif self.db.login_user(user_data[1], int(user_data[0])):
                self.logged = True
                await update.message.reply_text(bot_messages.set_login_success_msg(int(user_data[0])))
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGINING_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGIN_INPUT_MSG)


    async def balance(self, update : Update, context : ContextTypes.DEFAULT_TYPE):
        if self.logged:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="On your account X rubles")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_AUTHORIZED)
            

    async def history(self, update : Update, context : ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.get_history(history=history))


    async def stats(self, update : Update, context : ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='график.png')
        user_data = context.args
        if len(user_data) == 1:
            generate_stats_by_month(user_data, history=history)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo='график.png')
            os.remove(path='график.png')
        else:
            pass
            
    @staticmethod
    async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(bot_messages.HELLO_MSG)

