import sys

sys.path.append('../')

import vk_bot


def create_message(text='Hello', payload='{}'):
    message = {'date': 6666666666, 'from_id': 1, 'id': 1, 'out': 0, 'peer_id': 1, 'text': text,
               'conversation_message_id': 1, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
               'is_hidden': False, 'payload': payload}
    return message


def test_message_handler_commands(bot: vk_bot.VkBot):
    @bot.message_handler(commands=['start'])
    def command_handler(message):
        message.text_lower = 'got'

    msg = vk_bot.Message.from_dict(create_message(text='!start something'))
    bot._process_new_message(msg)

    assert msg.command == 'start' and msg.text == 'something' and msg.text_lower == 'got'


def test_message_handler_commands_two_handlers(bot: vk_bot.VkBot):
    @bot.message_handler(commands=['start'])
    def command_handler(message):
        message.text_lower = 'not got'

    @bot.message_handler(commands=['help'])
    def help_handler(message):
        message.text_lower = 'got'

    msg = vk_bot.Message.from_dict(create_message(text='!help something'))
    bot._process_new_message(msg)

    assert msg.command == 'help' and msg.text == 'something' and msg.text_lower == 'got'


def test_message_handler_commands_no_text(bot: vk_bot.VkBot):
    @bot.message_handler(commands=['start'])
    def command_handler(message):
        message.text_lower = 'got'

    msg = vk_bot.Message.from_dict(create_message(text='!start'))
    bot._process_new_message(msg)

    assert msg.command == 'start' and msg.text == '' and msg.text_lower == 'got'


def test_message_handler_payload(bot: vk_bot.VkBot):
    @bot.message_handler(payload_commands=['start'])
    def command_handler(message):
        message.text = 'got'

    msg = vk_bot.Message.from_dict(create_message(payload='{"command": "start"}'))
    bot._process_new_message(msg)

    assert msg.text == 'got'


def test_message_handler_regexp(bot: vk_bot.VkBot):
    @bot.message_handler(regexp=r'((https?):((//)|(\\))+([\w\d:#@%/;$()~_?\+-=\\.&](#!)?)*)')
    def command_handler(message):
        message.text = 'got'

    msg = vk_bot.Message.from_dict(create_message(text='https://vk.com/'))
    bot._process_new_message(msg)

    assert msg.text == 'got'


def test_message_handler_func(bot: vk_bot.VkBot):
    @bot.message_handler(func=lambda msg: msg.text.find('lambda') != -1)
    def command_handler(message):
        message.text = 'got'

    msg = vk_bot.Message.from_dict(create_message(text='lambda in message'))
    bot._process_new_message(msg)

    assert msg.text == 'got'
