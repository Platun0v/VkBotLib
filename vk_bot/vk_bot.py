import requests

import vk_api

from vk_bot import types


class VkBot:
    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id

        self.vk_api = vk_api.VkApi(token=token)
        self.api = self.vk_api.get_api()

        self.wait = None
        self.url = None
        self.key = None
        self.server = None
        self.ts = None

    def update_longpoll_server(self, update_ts=True):
        values = {
            'group_id': self.group_id
        }
        response = self.vk_api.method('groups.getLongPollServer', values)

        self.key = response['key']
        self.server = response['server']

        self.url = self.server

        if update_ts:
            self.ts = response['ts']

    def get_events(self):
        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
        }

        resp = requests.get(
            self.url,
            params=values,
            timeout=self.wait + 10
        ).json()

        if 'failed' not in resp:
            self.ts = resp['ts']
            return resp['updates']

        elif resp['failed'] == 1:
            self.ts = resp['ts']

        elif resp['failed'] == 2:
            self.update_longpoll_server(update_ts=False)

        elif resp['failed'] == 3:
            self.update_longpoll_server()

        return []

    def polling(self, wait=25):
        self.wait = wait
        self.update_longpoll_server()
        while True:
            for event in self.get_events():
                pass
