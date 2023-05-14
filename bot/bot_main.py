import os
import asyncio
import random

from telegram import Update, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent, \
    InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, \
    InlineQueryHandler
from telegram.ext.filters import BaseFilter

from bot import bot_messages
from db.db_api import Database
from bot.stats import generate_stats_by_month

history = ['Income 03.03.2023 150', 'Expense 07.03.2023 50', 'Expose 10.03.2023 50', 'Income 15.03.2023 100',
           'Income 25.03.2023 100', 'Income 26.03.2023 200', 'Expense 27.03.2023 150', 'Expense 30.03.2023 110']


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
        self.bot.add_handler(CommandHandler(bot_messages.REPEAT_CMD, self.repeat))
        self.bot.add_handler(MessageHandler(BaseFilter(), self.check_confirmation_code))
        self.bot.add_handler(CallbackQueryHandler(self.button_handler))
        self.bot.add_handler(InlineQueryHandler(self.inline_transfer))

    async def check_confirmation_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if confirmation_code_data := context.user_data.get("confirmation_code_data"):
            try:
                input_code = int(update.message.text.strip())
                if input_code == confirmation_code_data[0]:
                    context.user_data["user"] = confirmation_code_data[1]
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=bot_messages.SUCCESS_LOGIN_MSG)
                    asyncio.create_task(self.delay_quit(900, update, context))
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=bot_messages.WRONG_CONFIRMATION_CODE_MSG)
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.WRONG_CONFIRMATION_CODE_MSG)
            context.user_data.pop("confirmation_code_data")

    async def login(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_args = context.args
        if len(message_args) == 2:
            if context.user_data.get("user"):
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.ALREADY_LOGIN_USER_MSG)
            elif user := self.db.login_user(message_args[0], message_args[1]):
                confirmation_code = random.randint(100000, 999999)
                context.user_data["confirmation_code_data"] = [confirmation_code, user]
                await self.send_sms_confirmation(confirmation_code)
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.INPUT_CONFIRMATION_CODE)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGINING_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_LOGIN_INPUT_MSG)

    @staticmethod
    async def quit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data["user"]:
            context.user_data.pop("user")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.QUIT_SUCCESSFUL_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_AUTHORIZED_MSG)

    async def transfer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_args = context.args
        user = context.user_data.get("user")
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_AUTHORIZED_MSG)
        elif len(message_args) == 2:
            user = self.db.login_user(user.login, user.password)
            try:
                to_card = message_args[0]
                balance_changing = int(message_args[1])
            except ValueError:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.TRANSFER_INPUT_ERROR_MSG)
                return
            if to_card == user.card_number:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.TRANSFER_ON_YOUR_CARD_ERROR_MSG)
                return
            if balance_changing < 1:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.INCORRECT_TRANSFER_INPUT_MSG)
                return
            if balance_changing > user.balance:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.NOT_ENOUGH_MONEY_MSG)
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
            user = self.db.login_user(user.login, user.password)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=bot_messages.balance_msg(user.balance))
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_AUTHORIZED_MSG)

    async def history(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = context.user_data.get("user")
        if user:
            user = self.db.login_user(user.login, user.password)
            operations = self.db.get_all_operations(context.user_data["user"], 5)
            message = f"Последние {min(len(operations), 5)} операций:\n"
            for i in range(min(len(operations), 5)):
                if user.card_number == operations[i].from_user.card_number:
                    message += f"Перевод на карту {operations[i].to_user.card_number} " \
                               f"на сумму {operations[i].amount} рублей\n"
                else:
                    message += f"Пополнение с карты {operations[i].from_user.card_number} " \
                               f"на сумму {operations[i].amount} рублей\n"

            await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_AUTHORIZED_MSG)

    @staticmethod
    async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_args = context.args
        if len(message_args) == 1:
            generate_stats_by_month(int(message_args[0]), history=history)
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo='график.png')
            os.remove(path='график.png')
        else:
            pass

    @staticmethod
    async def delay_quit(delay: int, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await asyncio.sleep(delay)
        context.user_data.pop("user")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.QUIT_DELAY_MSG)

    @staticmethod
    async def send_sms_confirmation(code: int):
        print(code)

    async def inline_transfer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.inline_query.query.split()
        if len(query) < 1 or not context.user_data.get("user"):
            return
        elif len(query) == 1:
            results = [
                InlineQueryResultArticle(
                    id='2',
                    title='Получить',
                    input_message_content=InputTextMessageContent(bot_messages.payment_confirm(query[0])),
                    reply_markup=InlineKeyboardMarkup(self.gen_payment_inline_buttons(
                        context.user_data["user"].name, context.user_data["user"].card_number, query[0],
                    ))
                )
            ]
        else:
            results = [
                InlineQueryResultArticle(
                    id='1',
                    title='Перевести',
                    input_message_content=InputTextMessageContent(bot_messages.send_confirm(query[0], query[1])),
                    reply_markup=InlineKeyboardMarkup(self.gen_inline_buttons(
                        context.user_data["user"].name, query[0], query[1]
                    ))
                )
            ]

        await context.bot.answer_inline_query(update.inline_query.id, results)

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query_data = update.callback_query.data.split()
        from_user = query_data[1]
        await update.callback_query.answer()
        user = context.user_data.get("user")

        if not user or (from_user != user.name and query_data[0] == bot_messages.TRANSFER_SERVICE_ACCEPTED_CB) \
                or (query_data[0] == bot_messages.PAYMENT_SERVICE_ACCEPTED_CB and from_user == user.name):
            return

        user = self.db.login_user(user.login, user.password)
        if query_data[0] == bot_messages.TRANSFER_SERVICE_ACCEPTED_CB:
            try:
                to_card = int(query_data[2])
                amount = int(query_data[3])
            except ValueError:
                await update.callback_query.edit_message_text(bot_messages.WRONG_TRANSFER_INPUT_MSG)
                return

            if user.balance < amount:
                await update.callback_query.edit_message_text(bot_messages.NOT_ENOUGH_MONEY_MSG)
            elif amount < 0 or to_card == user.card_number:
                await update.callback_query.edit_message_text(bot_messages.WRONG_TRANSFER_INPUT_MSG)
            elif self.db.is_user_exists(card_number=to_card):
                self.db.change_balance(user, to_card, amount)
                await update.callback_query.edit_message_text(bot_messages.SUCCESSFULLY_TRANSFER_MSG)
            else:
                await update.callback_query.edit_message_text(bot_messages.USER_DOES_NOT_EXIST)
        elif query_data[0] == bot_messages.TRANSFER_SERVICE_CANCELED_CB:
            await update.callback_query.edit_message_text(bot_messages.CANCELED_TRANSFER_MSG)
        elif query_data[0] == bot_messages.PAYMENT_SERVICE_ACCEPTED_CB:
            try:
                to_card = query_data[2]
                amount = int(query_data[3])
            except ValueError:
                await update.callback_query.edit_message_text(bot_messages.WRONG_TRANSFER_INPUT_MSG)
                return
            
            if user.balance < amount:
                await update.callback_query.edit_message_text(bot_messages.NOT_ENOUGH_MONEY_MSG)
            elif amount <= 0:
                await update.callback_query.edit_message_text(bot_messages.WRONG_PAYMENT_INPUT_MSG)
            else:
                self.db.change_balance(user, to_card, amount)
                await update.callback_query.edit_message_text(bot_messages.SUCCESSFULLY_TRANSFER_MSG)

    async def repeat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = context.user_data.get("user")
        if user:
            user = self.db.login_user(user.login, user.password)
            if update.message.reply_to_message:
                msg = update.message.reply_to_message.text.split()
                if msg[0] != '/transfer':
                    await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.WRONG_REPEAT_MSG)
                    return
                msg = msg[1:]
                try:
                    to_card = msg[0]
                    balance_changing = int(msg[1])
                except ValueError:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=bot_messages.TRANSFER_INPUT_ERROR_MSG)
                    return
                if balance_changing < 1:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=bot_messages.INCORRECT_TRANSFER_INPUT_MSG)
                    return
                if balance_changing > user.balance:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=bot_messages.NOT_ENOUGH_MONEY_MSG)
                    return
                if self.db.is_user_exists(card_number=to_card):
                    self.db.change_balance(user, to_card, balance_changing)
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=bot_messages.transfer_success_msg(to_card))
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text=bot_messages.USER_DOES_NOT_EXIST)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=bot_messages.ISNT_REPLY_MESSAGE_MSG)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.NOT_AUTHORIZED_MSG)

    @staticmethod
    def gen_inline_buttons(username, to_card, amount):
        return [[
            InlineKeyboardButton(bot_messages.YES_MSG, callback_data=' '.join(
                [bot_messages.TRANSFER_SERVICE_ACCEPTED_CB, username, to_card, amount]
            )),
            InlineKeyboardButton(bot_messages.NO_MSG, callback_data=' '.join(
                [bot_messages.TRANSFER_SERVICE_CANCELED_CB, username, to_card, amount]
            )),
        ]]

    @staticmethod
    def gen_payment_inline_buttons(name, to_card, amount):
        return [[
            InlineKeyboardButton(bot_messages.PAY_MSG, callback_data=' '.join(
                [bot_messages.PAYMENT_SERVICE_ACCEPTED_CB, name, to_card, amount]
            )),
        ]]

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_messages.START_MSG)
