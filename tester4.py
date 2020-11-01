#
# Kirichenko_VS
# API for checking runtime and memory spent
# Version 0.3
#

import time
import sys
import os
import psutil
import importlib
import gc
import tracemalloc
import linecache
from flask import Flask, abort, request 
import json

app = Flask(__name__)

_timing = []
_module = sys

tracemalloc.start()

class timer:
    def __init__(self, _is_multiple_run = False):
        self.start = 0
        self._is_multiple_run = _is_multiple_run
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        _ = time.time() - self.start
        if self._is_multiple_run:
            _timing.append(_)
        else:
            print('Tester~ Run-time: {} sec.'.format(_))

#
# mode:
#   0 - постоянные аргументы
#   1 - итерируемый 1 объект
#
def __run__(obj:str, runs_number:int, mode:int, _print:bool, *args):
    global _timing
    global _module
    assert not(runs_number is None or obj is None or runs_number <= 0)
    if _print:
        print(f'Tester~ Run of the object "{obj}" {runs_number} times '+\
            f'with {"iterator" if mode == 1 else "non-iterator"} args: {args}')
    for i in range(runs_number):
        with timer(True):
            if mode == 0:
                res = _module.main(*args)
                #print(f'Tester~ Script with args {args} return: {res}')
            elif mode == 1:
                for i in range(args[0], args[1]):
                    res = _module.main(i)
                    #print(f'Tester~ Script with args {i} return: {res}')
    snapshot = tracemalloc.take_snapshot()
    if _print:
        print(f'Tester~ Average run-time: {sum(_timing)/runs_number} sec')
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print(f'Tester~ Memory usage: '+\
            f'{sum([l.size if l.traceback[0].filename.find(f"{obj}.py") != -1 else 0 for l in top_stats])} '+\
                f'byte')

def start(obj:str, runs_number:int, mode:int, *args):
    global _timing
    global _module
    _timing = []
    obj = 'tester_file.'+obj
    _module = importlib.import_module(obj)
    __run__(obj, runs_number, mode, True, *args[0])

@app.route('/post', methods=['POST']) 
def foo():
    if not request.json:
        abort(400)
    _input = request.json
    start(_input.get('file_name'), _input.get('runs_number'), _input.get('mode'), _input.get('args'))
    return json.dumps(request.json)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5005, debug=True)
