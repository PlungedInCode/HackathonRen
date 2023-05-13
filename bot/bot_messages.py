START_CMD = "start"
REGISTER_CMD = "register"
BALANCE_CMD = "balance"
HISTORY_CMD = "history"
LOGIN_CMD = "login"
QUIT_CMD = "quit"
STATS_CMD = "stats"

WRONG_LOGIN_INPUT_MSG = "Please enter correct data [card_number, password]"
WRONG_LOGINING_MSG = "Incorrect password or number of card"
ALREADY_EXISTS_USER_MSG = "User already exist"
SUCCESS_LOGIN = "Logining success"
ALREADY_LOGIN_USER_MSG = "You already logged"
QUIT_SUCCESSFUL_MSG = "Quit successful"
NOT_ALREADY_LOGING_NSG = "You are not already loging"
INCORRECT_INPUT_MSG = "Please enter correct data [card_number, name, login, password]"
NOT_AUTHORIZED = "Please authorize first"

HELLO_MSG = "Hello World!"

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