import re
import traceback
from random import randint
from typing import Optional, List, Callable, Dict, Any

import vk_api  # type: ignore

from vk_bot import types
from .api import Api, LongPoll
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
        self.api = Api(self.token, api_v)
        self._longpoll = LongPoll(self.api, group_id)

        self._message_handlers: List[Dict] = []

        self._command_start = command_start

    def longpoll_server(self, wait: int = 25):
        """

        :param wait: Время ожидания
        :return:
        """
        # TODO: Write description
        self._longpoll.wait = wait
        self._longpoll.update_longpoll_server()
        while True:
            for event in self._longpoll.get_events_longpoll():
                self._process_event(event)

    def infinity_longpoll_server(self, wait: int = 25):
        """

        :param wait: Время ожидания
        :return:
        """
        # TODO: Write description
        self._longpoll.wait = wait
        self._longpoll.update_longpoll_server()
        while True:
            try:
                for event in self._longpoll.get_events_longpoll():
                    self._process_event(event)
            except Exception as e:
                logger.error(e)
                with open('errors.txt', 'a') as f:
                    traceback.print_exc(file=f)
                    f.write(f'\n{"=" * 30}\n')
                self._longpoll.update_longpoll_server()

    @staticmethod
    def _exec_task(task, *args, **kwargs):
        task(*args, **kwargs)

    def _process_event(self, event):
        if event['type'] == 'message_new':
            self._process_new_message(types.Message.from_dict(event['object']))

    @staticmethod
    def _build_handler_dict(handler: Callable, **filters):
        return {
            'function': handler,
            'filters': filters
        }

    def message_handler(self, commands: Optional[List[str]] = None, payload_commands: Optional[List] = None,
                        regexp: Optional[str] = None, func: Optional[Callable[[types.Message], Any]] = None):
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
    def send_message(self, peer_id: Optional[int] = None, message: Optional[str] = None, keyboard=None, attachment=None,
                     **kwargs):
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
        return self.api.method('messages.send', values)
