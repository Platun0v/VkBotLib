import requests

import vk_api

from vk_bot import types


class VkBot:
    def __init__(self, token: str, group_id: int, api_v: str = '5.95'):
        """

        :param token: Токен группы
        :type token: str

        :param group_id: Id группы
        :type group_id: int

        :param api_v: Версия api ВКонтакте
        :type api_v: str
        """
        # TODO: Write description
        self.token = token
        self.group_id = group_id
        self.api_v = api_v

        self.vk_api = vk_api.VkApi(token=token, api_version=api_v)
        self.api = self.vk_api.get_api()

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

    def longpoll_server(self, wait=25):
        """

        :param wait: Время ожидания
        :type wait: int
        :return:
        """
        # TODO: Write description
        self._wait = wait
        self._update_longpoll_server()
        while True:
            for event in self._get_events_longpoll():
                self._process_event(event)

    def callback_request(self, request: dict, confirm_string: str, secret_string: str = None):
        """


        :param request: Запрос к серверу отправленный ВКонтакте
        :type request: dict

        :param confirm_string: Строка для подтверждения адреса сервера
        :type confirm_string: str

        :param secret_string: Секретный ключ бота
        :type secret_string: str

        :return: Ответ для ВКонтакте
        """
        # TODO: Write description
        if secret_string and 'secret' in request.keys():
            if request['keys'] != secret_string:
                return 'Bad request'

        if 'group_id' not in request.keys() or 'object' not in request.keys() or 'type' not in request.keys():
            return 'Bad request'

        if request['type'] == 'confirmation':
            return confirm_string
        else:
            self._process_event(request)

        return 'ok'

    def _process_event(self, event):
        pass
