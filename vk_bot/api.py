from typing import Optional, Dict

import requests

from . import logger


API_URL = 'https://api.vk.com/method/'


class Api:
    def __init__(self, token, api_version):
        self.token = token
        self.api_version = api_version
        self.session = requests.Session()

    def _make_request(self, method_name: str, method: str = 'get', params: Optional[Dict] = None):
        request_url = API_URL + method_name
        params = params.copy() if params else {}

        if 'v' not in params:
            params['v'] = self.api_version
        if 'access_token' not in params:
            params['access_token'] = self.token

        logger.debug(f"Request: method={method} url={request_url} params={params}")
        result = self.session.request(method, request_url, params=params)
        logger.debug("The server returned: '{0}'".format(result.text.encode('utf8')))


