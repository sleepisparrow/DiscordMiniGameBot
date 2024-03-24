import unittest
from unittest.mock import Mock, AsyncMock
from Commands.Versus import *


class TestVersus(unittest.IsolatedAsyncioTestCase):

    async def test_raise_exception_when_same_users(self):
        bot = Mock()
        interaction = Mock()
        interaction.response.defer = AsyncMock()
        interaction.response.send_message = AsyncMock()
        interaction.followup.send = AsyncMock()
        user = Mock(disnake.User)

        versus = Versus(bot=bot)
        await versus.start_versus(
            interaction=interaction,
            inter=interaction,
            user1=user,
            user2=user,
            user1_penalty="",
            user2_penalty="",
            minimum_wining_score=3,
            game_to_play="러시안룰렛"
        )

        interaction.response.send_message.assert_called_with("같은 사람을 선택할 수 없습니다.", ephemeral=True)