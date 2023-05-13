START_CMD = "start"
TRANSFER_CMD = "transfer"
BALANCE_CMD = "balance"
HISTORY_CMD = "history"
LOGIN_CMD = "login"
QUIT_CMD = "quit"
STATS_CMD = "stats"
REPEAT_CMD = "repeat"

YES_MSG = 'Да'
NO_MSG = 'Нет'

TRANSFER_SERVICE_ACCEPTED_CB = 'transfer_accepted'
TRANSFER_SERVICE_CANCELED_CB = 'transfer_canceled'

WRONG_LOGIN_INPUT_MSG = "Введите данные в формате: <логин>, <пароль>"
WRONG_LOGINING_MSG = "Неверный логин или пароль"
SUCCESS_LOGIN_MSG = "Вы успешно вошли\n" \
                    "В целях безопасности, через 15 минут автоматически будет произведен выход из аккаунта"
ALREADY_LOGIN_USER_MSG = "Вы уже в аккаунте"
QUIT_SUCCESSFUL_MSG = "Вы успешно вышли"
NOT_ALREADY_LOGING_MSG = "Вы не в аккаунте"
TRANSFER_INPUT_ERROR_MSG = "Введите данные в формате: <card_number>, <transfer_sum>"
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
WRONG_TRANSFER_INPUT_MSG = "Введите корректные данные в формате: <номер карты> <кол-во>"
SUCCESSFULLY_TRANSFER_MSG = "Деньги успешно переведены"
NOT_ENOUGH_MONEY_MSG = "Недостаточно средств"

START_MSG = "Я - бот РенесансКредит\n" \
            "Здесь ты можешь посмотреть баланс, историю переводов и статистику, выполнить перевод," \
            "а также получать уведомления об операциях"


def balance_msg(balance: int) -> str:
    return f"Ваш баланс {balance}"


def transfer_success_msg(to_card: int) -> str:
    return f"Перевод на карту {to_card} выполнен"


def get_history(history):
    result = ""
    for i in history:
        result += i
        result += '\n'
    return result


def send_confirm(to_card: str, amount: str):
    return f"Вы хотите отправить {to_card} {amount}?"
