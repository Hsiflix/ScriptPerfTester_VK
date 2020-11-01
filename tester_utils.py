#
# Kirichenko_VS
# Tester utils
# Version 0.1
#

import common_bus
import vk_api
import aut
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
import hashlib
import os

_session = None
_longpoll = None
_dirname = os.path.dirname(__file__)
_tester_file = os.path.join(_dirname, 'tester_file/')

class VkBotLongPollRaw(VkBotLongPoll):
    CLASS_BY_EVENT_TYPE = {}

def open_session():
    global _session
    global _longpoll
    vk_session_group = vk_api.VkApi(token = aut.token); #По токену открываем сессию
    vk_session_group._auth_token()
    _session = vk_session_group.get_api()
    _longpoll = VkBotLongPollRaw(vk_session_group, aut.group_id)
    return _session, _longpoll

def get_session():
    global _session
    return _session

def get_longpoll():
    global _longpoll
    return _longpoll

def send_msg(send_id, message, keyboard):
    global _session
    """
    Отправка сообщения через метод messages.send
    :param send_id: vk id пользователя, который получит сообщение
    :param message: содержимое отправляемого письма
    :param keyboard: отправить клавиатуру пользователю
    :return: None
    """
    if _session:
        _session.messages.send(peer_id=send_id,
                                message=message,
                                random_id = get_random_id(),
                                keyboard = keyboard)

def get_tester_file():
    global _tester_file
    return _tester_file

def get_new_file_name(access_key:str):
    hash = hashlib.sha256()
    hash.update(bytes(access_key, encoding='UTF-8'))
    return hash.hexdigest()