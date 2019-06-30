import pytest
import vk_bot


def create_message(text):
    message = {'date': 1561822569, 'from_id': 1, 'id': 1, 'out': 0, 'peer_id': 1, 'text': text,
               'conversation_message_id': 1, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [],
               'is_hidden': False}
    return message


def test_message_handler(bot: vk_bot.VkBot):
    @bot.message_handler(commands=['start'])
    def command_handler(message):
        message.text = 'got'

    msg = vk_bot.Message.from_dict(create_message('/start'))
    bot._process_new_message(msg)

    assert msg.text == 'got'
