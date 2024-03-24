from disnake import Embed
from disnake.ext import commands
import random


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter):
        await inter.response.send_message(f"🏓 Pong! ({round(inter.bot.latency * 1000)}ms)")

    @commands.slash_command()
    async def dice(
            self,
            inter,
            minimum: int,
            maximum: int,
            count: int = 1
    ):
        await inter.response.defer()
        # 1. 에러 체크
        if count <= 1:
            # TODO: print error message
            pass
        # 2. embed 제작
        string = "```\n"
        for i in range(count):
            number = random.randrange(minimum, maximum + 1)
            string += f"{i + 1}번째 주사위: {number}\n"
        string += "\n```"
        # 3. 출력
        embed = Embed(title=f"주사위! 최솟값: {minimum}, 최댓값: {maximum}", description=string)
        try:
            await inter.followup.send(embed=embed)
        except Exception as e:
            await inter.followup.send("에러가 발생했습니다. 더 작은 수로 다시 시도해주세요.")


def setup(bot):
    bot.add_cog(Basic(bot))
