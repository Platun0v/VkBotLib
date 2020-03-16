from random import randint
import re
import traceback
import sys

import requests

import vk_api

from vk_bot import types
from .logging import logger, log


class VkBot:
    def __init__(self, token: str, group_id: int, api_v: str = '5.103', command_start='/'):
        """

        :param token: Токен группы
        :param group_id: Id группы
        :param api_v: Версия api ВКонтакте
        :param command_start: Строка, с которой должна начинаться комманда
        """
        # TODO: Write description
        self.token = token
        self.group_id = group_id
        self.api_v = api_v

        self.vk_api = vk_api.VkApi(token=token, api_version=api_v)
        self.api = self.vk_api.get_api()

        self._message_handlers = []

        self._command_start = command_start

        self._wait = None
        self._url = None
        self._key = None
        self._server = None
        self._ts = None

    def _update_longpoll_server(self, update_ts=True):
        values = {
            'group_id': self.group_id
        }
        response = self.vk_api.method('groups.getLongPollServer', values)

        self._key = response['key']
        self._server = response['server']

        self._url = self._server

        if update_ts:
            self._ts = response['ts']

    def _get_events_longpoll(self):
        values = {
            'act': 'a_check',
            'key': self._key,
            'ts': self._ts,
            'wait': self._wait,
        }

        resp = requests.get(
            self._url,
            params=values,
            timeout=self._wait + 10
        ).json()

        if 'failed' not in resp:
            self._ts = resp['ts']
            return resp['updates']

        elif resp['failed'] == 1:
            self._ts = resp['ts']

        elif resp['failed'] == 2:
            self._update_longpoll_server(update_ts=False)

        elif resp['failed'] == 3:
            self._update_longpoll_server()

        return []

    def longpoll_server(self, wait: int = 25):
        """

        :param wait: Время ожидания
        :return:
        """
        # TODO: Write description
        self._wait = wait
        self._update_longpoll_server()
        while True:
            for event in self._get_events_longpoll():
                self._process_event(event)

    def infinity_longpoll_server(self, wait: int = 25):
        """

        :param wait: Время ожидания
        :return:
        """
        # TODO: Write description
        self._wait = wait
        self._update_longpoll_server()
        while True:
            try:
                for event in self._get_events_longpoll():
                    self._process_event(event)
            except Exception as e:
                logger.error(e)
                with open('errors.txt', 'a') as f:
                    traceback.print_exc(file=f)
                    f.write(f'\n{"=" * 30}\n')
                self._update_longpoll_server()

    @staticmethod
    def _exec_task(task, *args, **kwargs):
        task(*args, **kwargs)

    def _process_event(self, event):
        if event['type'] == 'message_new':
            self._process_new_message(types.Message.from_dict(event['object']))

    @staticmethod
    def _build_handler_dict(handler, **filters):
        return {
            'function': handler,
            'filters': filters
        }

    def message_handler(self, commands: list = None, payload_commands: list = None, regexp=None, func=None):
        """

        :param commands:
        :param payload_commands:
        :param regexp:
        :param func:
        :return:
        """

        # TODO: Write description
        def decorator(handler):
            handler_dict = self._build_handler_dict(
                handler,
                commands=commands,
                payload_commands=payload_commands,
                regexp=regexp,
                func=func,
            )
            self._message_handlers.append(handler_dict)

            return handler

        return decorator

    @staticmethod
    def _get_command(text: str, command_start: str):
        if text[:len(command_start)] == command_start:
            return text.split()[0][len(command_start):]

    def _test_message_handler(self, message_handler, message: types.Message):
        test_cases = {
            'commands': lambda msg: msg.process_command(self._command_start) in filter_value,
            'payload_commands': lambda msg: msg.payload_command in filter_value,
            'regexp': lambda msg: msg.text and re.search(filter_value, msg.text_lower),
            'func': lambda msg: filter_value(msg),
        }

        for filter, filter_value in message_handler['filters'].items():
            if filter_value is None:
                continue

            if not test_cases.get(filter, lambda msg: False)(message):
                return False

        return True

    def _process_new_message(self, message: types.Message):
        for message_handler in self._message_handlers:
            if self._test_message_handler(message_handler, message):
                self._exec_task(message_handler['function'], message)
                break

    @log
    def send_message(self, peer_id=None, message=None, keyboard=None, attachment=None, **kwargs):
        # TODO: Write Description
        values = kwargs
        if peer_id:
            values['peer_id'] = peer_id
        if message:
            values['message'] = message
        if keyboard:
            values['keyboard'] = keyboard
        if attachment:
            values['attachment'] = attachment

        values['random_id'] = randint(1, 2147483647)
        return self.vk_api.method('messages.send', values)

