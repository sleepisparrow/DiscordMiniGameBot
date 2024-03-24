import unittest
from unittest.mock import Mock, AsyncMock

import disnake

from Controller.ScoreBoard import ScoreBoard


class TestScoreBoard(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.user1 = Mock(disnake.Member)
        self.user1.name = "user1"

        self.user2 = Mock(disnake.Member)
        self.user2.name = "user2"

        self.penalty1 = "penalty1"
        self.penalty2 = "penalty2"
        self.winning_score = 3
        self.game = "game"

        self.channel = Mock()
        self.channel.send = AsyncMock()

    async def test_print_score_board(self):
        score_board = ScoreBoard(
            channel=self.channel,
            user1=self.user1,
            user2=self.user2,
            user1_penalty=self.penalty1,
            user2_penalty=self.penalty2,
            winning_score=self.winning_score,
            game=self.game
        )
        await score_board.print_score_board()

        self.channel.send.assert_called_with(
            disnake.Embed(title="대결", description=f"유저 1: {self.user1.name}\n유저 2: {self.user2.name}")
            .add_field(name="벌칙",
                       value=f"```{self.user1.name}: {self.penalty1}\n{self.user2.name}: {self.penalty2}```",
                       inline=False)
            .add_field(name="점수",
                       value=f"```{self.user1.name}: 0\n{self.user2.name}: 0```",
                       inline=False)
            .add_field(name=f"승리 점수: {self.winning_score}", value="", inline=False)
            .add_field(name="게임", value=f"```{self.game}```", inline=False)
        )

    async def test_score_added(self):
        score_board = ScoreBoard(
            channel=self.channel,
            user1=self.user1,
            user2=self.user2,
            user1_penalty=self.penalty1,
            user2_penalty=self.penalty2,
            winning_score=self.winning_score,
            game=self.game
        )

        score_board.add_score(self.user1)
        await score_board.print_score_board()

        self.channel.send.assert_called_with(
            disnake.Embed(title="대결", description=f"유저 1: {self.user1.name}\n유저 2: {self.user2.name}")
            .add_field(name="벌칙",
                       value=f"```{self.user1.name}: {self.penalty1}\n{self.user2.name}: {self.penalty2}```",
                       inline=False)
            .add_field(name="점수",
                       value=f"```{self.user1.name}: 1\n{self.user2.name}: 0```",
                       inline=False)
            .add_field(name=f"승리 점수: {self.winning_score}", value="", inline=False)
            .add_field(name="게임", value=f"```{self.game}```", inline=False)
        )