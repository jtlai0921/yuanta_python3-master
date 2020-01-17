class LoginException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return 'Error message : ' + self.message

def login(username, password):
    if (username == 'admin' and password == '1234'):
        print('Pass')
    else:
        raise LoginException('Login Error')


try:
    login('admin', '5678')
except LoginException as value:
    print(value)
