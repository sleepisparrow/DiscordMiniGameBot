import disnake
from disnake.ext import commands

from Controller.RussianRouletteController import RussianRouletteController


class RussianRoulette(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="러시안_룰렛")
    async def russian_roulette(
            self,
            inter,
            user1: disnake.Member,
            user2: disnake.Member,
            true_bullet: int = commands.Param(name="진짜_총알"),
            total_bullet: int = commands.Param(name="전체_총알")
    ):
        # 이 함수에서는 파라미터만 에러가 없는지 확인하고, 그냥 Controller로 넘겨버림
        try:
            t = RussianRouletteController.start_russian_roulette(user1, user2, true_bullet, total_bullet)
            await inter.response.send_message(embed=t[0], view=t[1])
        except Exception as E:
            await inter.response.send_message(f"에러가 발생했습니다. {E}", ephemeral=True)
            return


def setup(bot):
    bot.add_cog(RussianRoulette(bot))
