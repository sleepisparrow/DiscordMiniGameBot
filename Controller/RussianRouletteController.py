import random
from typing import Callable

import disnake


class RussianRouletteController:
    is_one_vs_one = True

    @staticmethod
    def start_russian_roulette(
            user1: disnake.Member,
            user2: disnake.Member,
            true_bullet: int,
            total_bullet: int
    ) -> (disnake.Embed, disnake.ui.View):
        # 기본 예외 처리
        if user1 == user2:
            raise ValueError("같은 사람을 선택할 수 없습니다.")
        if true_bullet > total_bullet:
            raise ValueError("진짜 총알이 전체 총알보다 많을 수 없습니다.")
        if true_bullet < 1:
            raise ValueError("진짜 총알이 1보다 작을 수 없습니다.")

        # 러시안 룰렛 시작
        embed = disnake.Embed(title="러시안 룰렛", description=f"유저 1: {user1.name}\n유저 2: {user2.name}")
        return embed, RussianRouletteButton(user1, user2, true_bullet, total_bullet)


class RussianRouletteButton(disnake.ui.View):
    def __init__(self, user1: disnake.Member, user2: disnake.Member, true_bullet: int, total_bullet: int,
                 return_target: Callable[[int], None] = None):
        """

        Args:
            user1 (disnake.Member): 유저 1
            user2 (disnake.Member): 유저 2 (1과는 달라야 함)
            true_bullet (int): 맞으면 패배하는 진짜 총알의 수
            total_bullet (int): 가짜 총알 + 진짜 총알의 수
            return_target (Callable[[int]], optional): 게임의 결과를 이 메서드를 호출함으로서 반환한다.
        """
        super().__init__()
        self.user1 = user1
        self.user2 = user2
        self.turn = 0
        self.true_bullet = true_bullet
        self.bullet_position = random.sample(range(0, total_bullet), true_bullet)
        self.__return_target = return_target

    @disnake.ui.button(label="발사", style=disnake.ButtonStyle.red)
    async def fire(self, button: disnake.Button, interaction: disnake.Interaction):
        # 1. 자기 턴인 유저 체크
        if self.turn % 2 == 0:
            target_user = self.user1
        else:
            target_user = self.user2

        # 2. 다른 사람이 버튼 못 누르도록 제작
        if interaction.user != target_user:
            await interaction.response.send_message("자신의 턴인 사람만 발사를 누를 수 있습니다.", ephemeral=True)
            return

        # 3. 러시안 룰렛 진행
        if self.turn not in self.bullet_position:
            embed = disnake.Embed(title="러시안 룰렛", description=f"유저 1: {self.user1.name}\n유저 2: {self.user2.name}")
            embed.add_field(name=f"턴 {self.turn + 1}", value=f"{target_user.name}님이 쏜 탄환은 가짜 탄환입니다!", inline=False)
            self.turn += 1
            await interaction.response.edit_message(embed=embed, view=self)
            return

        embed = disnake.Embed(title="러시안 룰렛", description=f"유저 1: {self.user1.name}\n유저 2: {self.user2.name}")
        embed.add_field(name="결과", value=f"{target_user.name}님이 죽었습니다!", inline=False)
        await interaction.response.edit_message(embed=embed, view=None)

        # TODO: 만약 비동기로 return target을 호출하고, n초 후에 이걸 지워버리는건 어떨까?Z
        if self.__return_target is not None:
            await self.__return_target(self.turn % 2 + 1)
