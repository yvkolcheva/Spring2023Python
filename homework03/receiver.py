import time

import requests

after = 0

while True:
    response = requests.get(
        'http://127.0.0.1:5000/messages',
        params={'after': after}
    )
    messages = response.json()['messages']
    for message in messages:
        print(message['time'], message['name'])
        print(message['text'])
        print()
        after = message['time']
    time.sleep(1)

