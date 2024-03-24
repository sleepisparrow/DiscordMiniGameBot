import logging

import disnake


class ScoreBoard:
    def __init__(
            self,
            channel,
            user1: disnake.User,
            user2: disnake.User,
            user1_penalty: str,
            user2_penalty: str,
            winning_score: int,
            game: str
    ):
        self.__user1 = user1
        self.__user1_penalty = user1_penalty
        self.__user1_score = 0

        self.__user2 = user2
        self.__user2_penalty = user2_penalty
        self.__user2_score = 0

        self.__winning_score = winning_score
        self.__channel = channel
        self.__game = game

    async def print_score_board(self):
        """
        print score board to the channel where the game is played
        """
        await self.__channel.send(
            disnake.Embed(title="대결", description=f"유저 1: {self.__user1.name}\n유저 2: {self.__user2.name}")
            .add_field(
                name="벌칙",
                value=f"```{self.__user1.name}: {self.__user1_penalty}\n{self.__user2.name}: {self.__user2_penalty}```",
                inline=False
            )
            .add_field(
                name="점수",
                value=f"```{self.__user1.name}: {self.__user1_score}\n{self.__user2.name}: {self.__user2_score}```",
                inline=False
            )
            .add_field(name=f"승리 점수: {self.__winning_score}", value="", inline=False)
            .add_field(name="게임", value=f"```{self.__game}```", inline=False)
        )
    # TODO: winning 스코어를 채운 경우, 결과 embed가 뜨도록 수정하기
    #  print_score_board 함수를 다른 함수로 바꾸기

    def add_score(self, user: disnake.User):
        """
        add score to the user
        param user:  who scored (must be user1 or user 2)
        """
        if user == self.__user1:
            self.__user1_score += 1
        elif user == self.__user2:
            self.__user2_score += 1
        else:
            logging.error("User not in the game")
