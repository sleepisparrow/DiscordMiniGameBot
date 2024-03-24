import unittest
from unittest.mock import Mock, AsyncMock
from Commands.Versus import *


class TestVersus(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.bot = Mock()
        self.interaction = Mock()
        self.interaction.response.defer = AsyncMock()
        self.interaction.response.send_message = AsyncMock()
        self.interaction.followup.send = AsyncMock()

    async def test_raise_exception_when_same_users(self):
        user = Mock(disnake.User)

        versus = Versus(bot=self.bot)
        await versus.start_versus(
            interaction=self.interaction,
            inter=self.interaction,
            user1=user,
            user2=user,
            user1_penalty="",
            user2_penalty="",
            minimum_wining_score=3,
            game_to_play="러시안룰렛"
        )

        self.interaction.response.send_message.assert_called_with("같은 사람을 선택할 수 없습니다.", ephemeral=True)

    async def test_raise_exception_when_get_wrong_winning_score(self):
        user1 = Mock(disnake.User)
        user2 = Mock(disnake.User)

        versus = Versus(bot=self.bot)
        await versus.start_versus(
            interaction=self.interaction,
            inter=self.interaction,
            user1=user1,
            user2=user2,
            user1_penalty="",
            user2_penalty="",
            minimum_wining_score=0,
            game_to_play="러시안룰렛"
        )

        self.interaction.response.send_message.assert_called_with("승리 점수는 1 이상이어야 합니다.", ephemeral=True)