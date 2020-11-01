# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 21:34:46 2020

@author: Viktoe
"""

import common_bus
import tester_utils
import vk_api
import aut
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
import hashlib
import os

_dirname = os.path.dirname(__file__)
_filename = os.path.join(_dirname, 'tester_file/')

vk_group, longpoll = tester_utils.open_session()

while True:
    for event in longpoll.listen():
        print('========================================================')
        #print(event)
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.peer_id == event.object.from_id or event.object.peer_id != event.object.from_id:
                print('Новое сообщение: ', end = '')
                print(event.object.text) # Читаем сообщение
                print('От пользователя: ', end = '')
                try:
                    print(vk_group.users.get(user_id = event.object.from_id))
                except:
                    print('Error')
                if event.object.id > 0: #ЛС
                    attach = event.object.attachments
                    if len(attach) > 0 and attach[0].get('type') == 'doc' \
                        and attach[0].get('doc').get('ext') == 'py':
                        with open(f'{tester_utils.get_tester_file()}'+\
                            f'{tester_utils.get_new_file_name(attach[0].get("doc").get("access_key"))}.py', 'wb') as f:
                            ufr = requests.get(attach[0].get('doc').get('url'))
                            f.write(ufr.content)
                        tester_utils.send_msg(send_id = event.object.peer_id,
                                message = f'Получила файл {attach[0].get("doc").get("title")}',
                                keyboard = None)
                else: #Беседы
                    pass
