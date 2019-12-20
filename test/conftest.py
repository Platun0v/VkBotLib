import sys

sys.path.append('../')

import os
import pytest
import vk_bot


@pytest.fixture
def bot():
    token = os.getenv('VK_GROUP_TOKEN')
    group_id = os.getenv('GROUP_ID')
    bot = vk_bot.VkBot(token=token, group_id=group_id)
    return bot
