#
# Kirichenko_VS
# Модуль общей шины бота-тестера
# Задает и контролирует очередь проверки пользотельских скриптов
# Version 0.1
#

import time
from flask import Flask, abort, request 
import json

app = Flask(__name__)

_max_threads = 6
# _queue.key - уникальный индекс объекта
# _queue.value - dict-объект с ключами: 'timestamp', 'peer_id', 'file_title', 'count_runs', 'is_range', 'args'
_queue = {}

def add_object(peer_id:int, file_title:str):
    pass

@app.route('/post', methods=['POST']) 
def foo():
    if not request.json:
        abort(400)
    print(request.json)
    return json.dumps(request.json)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)