import os

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler
from bot import bot_messages
from db.db_api import Database
from bot.stats import generate_stats_by_month


history = ['Income 25.03.2023 100', 'Income 26.03.2023 200', 'Expense 27.03.2023 150']


class Bot:
    def __init__(self, db: Database):
        self.db = db
        self.bot = Application.builder() \
            .token(os.getenv("BOT_TOKEN")) \
            .build()
        self.bot.add_handler(CommandHandler(bot_messages.START_CMD, self.start))
        self.bot.add_handler(CommandHandler(bot_messages.QUIT_CMD, self.quit))
        self.bot.add_handler(CommandHandler(bot_messages.BALANCE_CMD, self.balance))
        self.bot.add_handler(CommandHandler(bot_messages.HISTORY_CMD, self.history))
        self.bot.add_handler(CommandHandler(bot_messages.LOGIN_CMD, self.login))
        self.bot.add_handler(CommandHandler(bot_messages.STATS_CMD, self.stats))
        self.bot.add_handler(CommandHandler(bot_messages.TRANSFER_CMD, self.transfer))

    async def login(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_args = context.args
        if len(message_args) == 2:
            if context.user_data.get("user"):
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.ALREADY_LOGIN_USER_MSG)
            elif user := self.db.login_user(message_args[0], message_args[1]):
                context.user_data["user"] = user
                await update.message.reply_text(bot_messages.set_login_success_msg(int(message_args[0])))
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGINING_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGIN_INPUT_MSG)

    async def quit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data["user"]:
            context.user_data.pop("user")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.QUIT_SUCCESSFUL_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_ALREADY_LOGING_MSG)

    async def transfer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_args = context.args
        user = context.user_data.get("user")
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_ALREADY_LOGING_MSG)
        elif len(message_args) == 2:
            try:
                to_card = int(message_args[0])
                balance_changing = int(message_args[1])
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.TRANSFER_INPUT_ERROR_MSG)
                return
            if self.db.is_user_exists(card_number=message_args[0]):
                self.db.change_balance(user, to_card, balance_changing)
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.transfer_success_msg(to_card))
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.USER_DOES_NOT_EXIST)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.TRANSFER_INPUT_ERROR_MSG)

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = context.user_data.get("user")
        if user:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"On your account {user.balance} rubles")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_AUTHORIZED)

    async def history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.get_history(history=history))

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text='график.png')
        message_args = context.args
        if len(message_args) == 1:
            generate_stats_by_month(message_args, history=history)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo='график.png')
            os.remove(path='график.png')
        else:
            pass

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.START_CMD)
