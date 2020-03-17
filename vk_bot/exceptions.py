class VkBotError(Exception):
    pass


class HttpError(VkBotError):
    def __init__(self, method, values, response):
        self.method = method
        self.values = values
        self.response = response

    def __str__(self):
        return 'Response code {}'.format(self.response.status_code)


class ApiError(VkBotError):
    def __init__(self, method, values, error):
        self.method = method
        self.values = values
        self.error = error
        self.code = error['error_code']
        self.error_msg = error['error_msg']

    def __str__(self):
        return f'[{self.code} {self.error_msg}]'
