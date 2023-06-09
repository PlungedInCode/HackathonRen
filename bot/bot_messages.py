START_CMD = "start"
TRANSFER_CMD = "transfer"
BALANCE_CMD = "balance"
HISTORY_CMD = "history"
LOGIN_CMD = "login"
QUIT_CMD = "quit"
STATS_CMD = "stats"
REPEAT_CMD = "repeat"
HELP_CMD = "help"

YES_MSG = 'Да'
NO_MSG = 'Нет'
PAY_MSG = 'Перевести'

TRANSFER_SERVICE_ACCEPTED_CB = 'transfer_accepted'
TRANSFER_SERVICE_CANCELED_CB = 'transfer_canceled'
PAYMENT_SERVICE_ACCEPTED_CB = 'payment_accepted'

WRONG_LOGIN_INPUT_MSG = "Введите данные в формате: <логин>, <пароль>"
WRONG_LOGINING_MSG = "Неверный логин или пароль"
SUCCESS_LOGIN_MSG = "Вы успешно вошли\n" \
                    "В целях безопасности, через 15 минут автоматически будет произведен выход из аккаунта"
ALREADY_LOGIN_USER_MSG = "Вы уже в аккаунте"
QUIT_SUCCESSFUL_MSG = "Вы успешно вышли"
TRANSFER_INPUT_ERROR_MSG = "Введите данные в формате: <номер карты>, <сумма>"
NOT_AUTHORIZED_MSG = "В начале надо войти в аккаунт"
USER_DOES_NOT_EXIST = "Пользователя с таким логином не существует"
INPUT_CONFIRMATION_CODE = "На Ваш номер был отправлен СМС с кодом подтверждения, введите его"
WRONG_CONFIRMATION_CODE_MSG = "Неверный код"
TRANSFER_ON_YOUR_CARD_ERROR_MSG = "Вы не можете выполнить перевод на свою же карту"
WRONG_REPEAT_MSG = "Вы переслали неверное сообщение, можно повторить только операцию transfer"
ISNT_REPLY_MESSAGE_MSG = "Команду repeat можно применять только для пересылаемых сообщений"
QUIT_DELAY_MSG = "После входа в аккаунт прошло 15 минут\n" \
                 "Был произведен автоматический выход"
INCORRECT_TRANSFER_INPUT_MSG = "Некорректно введена сумма для перевода"

CANCELED_TRANSFER_MSG = "Перевод отменен"
WRONG_TRANSFER_INPUT_MSG = "Введите корректные данные в формате: <номер карты> <сумма>"
SUCCESSFULLY_TRANSFER_MSG = "Деньги успешно переведены"
NOT_ENOUGH_MONEY_MSG = "Недостаточно средств"

START_MSG = "Я - бот РенесансКредит\n" \
            "Здесь ты можешь посмотреть баланс, историю переводов и статистику, выполнить перевод," \
            "а также получать уведомления об операциях"
HELP_MSG = "/login <логин> <пароль> - войти в аккаунт банка\n" \
           "/transfer <номер карты> <сумма> - выполнить перевод\n" \
           "/balance - проверить баланс\n" \
           "/history - получить последние операции\n" \
           "/stats <номер месяца> - получить статистику баланса за месяц\n" \
           "/repeat - повторить перевод\n" \
           "/quit - выйти из аккаунта банка\n" \
           "/help - просмотр доступных команд\n"

WRONG_PAYMENT_INPUT_MSG = "Введите корректные данные в формате: <сумма>"


def balance_msg(balance: int) -> str:
    return f"Ваш баланс {balance} рублей"


def transfer_success_msg(to_card: str) -> str:
    return f"Перевод на карту {to_card} выполнен"


def send_confirm(to_card: str, amount: str):
    return f"Вы хотите перевести {to_card} {amount} рублей?"


def payment_confirm(amount: str):
    return f"Перевести {amount} рублей?"