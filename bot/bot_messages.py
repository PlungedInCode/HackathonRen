START_CMD = "start"
TRANSFER_CMD = "transfer"
BALANCE_CMD = "balance"
HISTORY_CMD = "history"
LOGIN_CMD = "login"
QUIT_CMD = "quit"
STATS_CMD = "stats"

WRONG_LOGIN_INPUT_MSG = "Введите корректные данные в формате: <логин>, <пароль>"
WRONG_LOGINING_MSG = "Некорректный логин или пароль"
SUCCESS_LOGIN = "Вы успешно вошли"
ALREADY_LOGIN_USER_MSG = "Вы уже в аккаунте"
QUIT_SUCCESSFUL_MSG = "Вы успешно вышли"
NOT_ALREADY_LOGING_MSG = "Вы не в аккаунте"
TRANSFER_INPUT_ERROR_MSG = "Введите корректные данные в формате: <card_number>, <transfer_sum>"
NOT_AUTHORIZED = "В начале надо войти в аккаунт"
USER_DOES_NOT_EXIST = "Пользователя с таким логином не существует"

HELLO_MSG = ""


def transfer_success_msg(to_card: int):
    return f"Перевод на карту {to_card} выполнен"


def set_service_success_msg(login):
    return f"{login} saved"


def get_history(history):
    result = ""
    for i in history:
        result += i
        result += '\n'
    return result


def set_login_success_msg(login):
    return f"{login} login success"