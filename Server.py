from flask import Flask, request
from time import asctime, time
from datetime import datetime
import sys

app = Flask(__name__)
messages = [
    {"username": "Jack", "text": "Hello!", "time": time()},
    {"username": "Mary", "text": "Hi Jack!", "time": time()},
]

users = {
    'Jack': '12345',
    'Mary': '54321',
}

msg_counter = {
    'Jack': 1,
    'Mary': 1,
}


@app.route("/")
def hello_view():
    return "<h1>Welcome to Python Messenger!</h1>"

@app.route("/status")
def status_view():
    status_specs = {
        'status': True,
        'time': asctime(),
        'users_total': len(users),
        'messages_total': len(messages)
    }
    return status_specs



@app.route("/messages")
def messages_view():
    """
    Получение сообщений после отметки after
    input: after - отметка времени
    output: {
        "messages": [
        {"username" : str, "text" : str, "time" : float},
        ...
        ]
    }
    """
    after = float(request.args['after'])
    new_messages = [message for message in messages if message['time'] > after]
    return{'messages': new_messages}


@app.route("/send", methods=['POST'])
def send_view():
    """
    Отправка сообщений
    input: {
        "username" : str,
        "password" : str,
        "text" : str
    }
    output: {"ok" : bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users or users[username] != password:
        return{"ok" : False}

    text = data["text"]
    messages.append({"username" : username, "text" : text, "time" : time()})

    msg_counter[username] +=1 #message counter

    return{'ok' : True}


@app.route("/auth", methods=['POST'])
def auth_view():
    """
    Авторизовать пользователя или сообщить, что пароль неверный
    input: {
        "username": str
        "password" : str
    }
    output: {"ok" : bool}
    """
    data = request.json
    username = data["username"]
    password = data["password"]

    if username not in users:
        users[username] = password
        msg_counter[username] = 0 #message counter
        return{"ok" : True}
    elif users[username] == password:
        return{"ok" : True}
    else:
        return{"ok" : False}

@app.route("/users")
def users_view():
    """
    Показать пользователей на сайте и количество сообщений у каждого
    input: ---
    output:
        {"msg_counter": [
        {"username": str, "msg_counter": float},
        ...
        ]
    }
    """

    return{'users': msg_counter}


app.run()