START_CMD = "start"
REGISTER_CMD = "register"
LOGIN_CMD = "login"
QUIT_CMD = "quit"
TRANSFER_CMD = "transfer"

INCORRECT_INPUT_MSG = "Please enter correct data [card_number, name, login, password]"
WRONG_LOGIN_INPUT_MSG = "Please enter correct data [card_number, password]"
WRONG_LOGINING_MSG = "Incorrect password or number of card"
ALREADY_EXISTS_USER_MSG = "User already exist"
SUCCESS_LOGIN_MSG = "Logining success"
ALREADY_LOGIN_USER_MSG = "You already logged"
QUIT_SUCCESSFUL_MSG = "Quit successful"
NOT_ALREADY_LOGING_MSG = "You are not already loging"
TRANSFER_SUCCESSFUL_MSG = "Transfer is successful"
TRANSFER_INPUT_ERROR_MSG = "Please enter correct data [card_number, transfer_sum]"

HELLO_MSG = "Hello World!"

def set_service_success_msg(login):
    return f"{login} saved"

def set_login_success_msg(login):
    return f"{login} login success"