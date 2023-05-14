import time
from datetime import datetime
from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'time':time.time(),
        'name':'Julia',
        'text':'Создаю мессенджер',
    },
    {
        'time': time.time(),
        'name': 'Maks',
        'text': 'Всё ещё пытаюсь создать',
    },
    {
        'time': time.time(),
        'name': 'Maks',
        'text': 'И до сих пор...',
    }
]
@app.route("/")
def hello():
    return "Добро пожаловать!"

@app.route('/status')
def status():
    User = []
    count = 0
    for i in db:
        if i['name'] not in User:
            count+=1
            User.append(i['name'])

    dt_now = datetime.now()
    return{'status': True,
           'name':'Messenger',
           'time': dt_now,
           'number_of_users': count,
           'number_of_messages': len(db),
           'name_users': User,
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
    if message['text'] == '/help':
        message = {
            'time': time.time(),
            'name': 'Бот:',
            'text': 'Здравствуйте! Тут всё просто: \
            нажмите "Send" и сообщение отправится, и вы увидите его тут. Так же вы можете ввести "/game" и посмотреть что получится.'

        }
    if message['text'] == '/game':
        message = {
            'time': time.time(),
            'name': 'Бот:',
            'text': 'Мы бы поиграли, но у меня нет настроения, потому, простите, пользователь, не сегодня.'

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
