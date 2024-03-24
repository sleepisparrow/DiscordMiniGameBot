import disnake
from disnake.ext import commands

from Controller.VS_RussianRoulette import RussianRouletteStarter


class Versus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user1 = None
        self.user2 = None
        self.user1_score = 0
        self.user2_score = 0
        self.minimum_wining_score = None
        self.user1_penalty = None
        self.user2_penalty = None
        self.game_to_play = None

    def make_scoreboard(self, ) -> disnake.Embed:
        embed = disnake.Embed(title="대결", description=f"유저 1: {self.user1.name}\n유저 2: {self.user2.name}")
        embed.add_field(name="벌칙",
                        value=f"```{self.user1.name}: {self.user1_penalty}\n{self.user2.name}: {self.user2_penalty}```",
                        inline=False)
        embed.add_field(name="점수",
                        value=f"```{self.user1.name}: {self.user1_score}\n{self.user2.name}: {self.user2_score}```",
                        inline=False)
        embed.add_field(name=f"승리 점수: {self.minimum_wining_score}", value="", inline=False)
        embed.add_field(name="게임", value=f"```{self.game_to_play}```", inline=False)
        return embed

    @commands.slash_command(name="대결")
    async def start_versus(
            self,
            inter,
            user1: disnake.Member = commands.Param(name="유저1"),
            user2: disnake.Member = commands.Param(name="유저2"),
            user1_penalty: str = commands.Param(name="유저1_벌칙", description="유저 1이 질 경우 수행할 벌칙을 입력하세요", default="없음"),
            user2_penalty: str = commands.Param(name="유저2_벌칙", description="유저 2가 질 경우 수행할 벌칙을 입력하세요", default="없음"),
            minimum_wining_score: int = commands.Param(name="승리_점수", description="승리하기 위한 최소 승점을 입력하세요", default=3),
            game_to_play=commands.Param(name="게임", description="게임을 선택하세요", choices=["러시안_룰렛"])
    ):
        await inter.response.defer()

        # 기본 예외 처리
        if user1 == user2:
            await inter.response.send_message("같은 사람을 선택할 수 없습니다.", ephemeral=True)
            return
        if minimum_wining_score < 1:
            await inter.response.send_message("승리 점수는 1 이상이어야 합니다.", ephemeral=True)
            return

        # 데이터 등록
        self.user1 = user1
        self.user2 = user2
        self.minimum_wining_score = minimum_wining_score
        self.user1_penalty = user1_penalty
        self.user2_penalty = user2_penalty
        self.game_to_play = game_to_play

        # 기본 임베드 제작
        embed = self.make_scoreboard()

        # 게임 시작
        await inter.followup.send(embed=embed, view=VersusButton(user1, user2, game_to_play))


class VersusButton(disnake.ui.View):
    def __init__(self, user1: disnake.Member, user2: disnake.Member, game_to_play: str):
        super().__init__()
        self.user1 = user1
        self.user2 = user2
        self.game_to_play = game_to_play

    @disnake.ui.button(label="게임 시작", style=disnake.ButtonStyle.green)
    async def start_game(self, button: disnake.Button, interaction: disnake.Interaction):
        # 1. 게임 시작을 누른 사람이 유저 2인지 확인
        if interaction.user != self.user2:
            await interaction.response.send_message("게임 시작 권한이 없습니다.", ephemeral=True)
            return

        # 2. 게임 시작
        # TODO: 어떤 게임인지 찾기
        starter = RussianRouletteStarter(self.user1, self.user2, interaction.channel)
        await starter.start()

        # TODO:
        #  [ ] 게임이 끝났을 때 정보가 업데이트.


def setup(bot):
    bot.add_cog(Versus(bot))
