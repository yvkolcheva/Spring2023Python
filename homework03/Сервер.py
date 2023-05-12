import time
from datetime import datetime
from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'time':time.time(),
        'name':'Юлия',
        'text':'Создаю мессенджер',
    }
]
@app.route("/")
def hello():
    return "Добро пожаловать!"

@app.route('/status')
def status():
    dt_now = datetime.now()
    return{'status': True,
           'name':'Messenger',
           'time': dt_now,
           'users':0
           }

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)
    if len(data) != 2:
        return abort(400)

    name = data["name"]
    text = data["text"]

    if not isinstance(name, str) or not isinstance(text, str) or name == '' or text == '':
        return abort(400)

    message = {
        'time': time.time(),
        'name': name,
        'text': text,
    }
    db. append(message)
    return {'ok': True}

@app.route('/messages')
def get_message():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    result = []
    for message in db:
        if message['time'] > after:
            result. append(message)
            if len(result) >= 100:
                break
    return {'messages': result}

app.run()
#h