from venv import logger
import disnake
from Controller.RussianRouletteController import RussianRouletteController

from Daemon.Observer import Observer
from Daemon.OnMessageListener import OnMessageListener


class RussianRouletteParamObserver(Observer):
    def __init__(self, game_user: list[disnake.Member], init_message: disnake.Message):
        self.param = []
        self.game_user = game_user
        self.previous_msg = [init_message]

    async def update(self, message):
        if message.author not in self.game_user:
            return
        number: int
        try:
            number = int(message.content)
            self.previous_msg.append(message)
        except ValueError:
            await self.__send_message(message.channel, "숫자를 입력해주세요")
            return

        # Parameter 개수에 따라서 진행함
        match len(self.param):
            case 0:  # 진짜 총알을 받을 때
                if number < 1:
                    await self.__send_message(message.channel, "진짜 총알이 적어도 1개 이상 필요합니다.")
                    return
                self.param.append(number)
                await self.__send_message(message.channel, "전체 총알의 수를 정해주세요")
            case 1:  # 전체 총알을 받을 때
                if number <= self.param[0]:
                    await self.__send_message(message.channel, "전체 총알이 진짜 총알보다 적을 순 없습니다.")
                    return
                self.param.append(number)
                OnMessageListener.remove_observer(self)
                msg_component = RussianRouletteController.start_russian_roulette(
                    self.game_user[0],
                    self.game_user[1],
                    self.param[0],
                    self.param[1]
                )
                # 질문을 하며 받은 메세지들 삭제 과정
                for msg in self.previous_msg:
                    await msg.delete()
                await message.channel.send(embed=msg_component[0], view=msg_component[1])
            case _:  # 오류 발생!
                logger.warning("RussianRouletteParamObserver의 param이 2개 이상입니다. 이 경우, observer가 삭제되지 않아 발생한 문제일 수 있습니다.")
                OnMessageListener.remove_observer(self)

    async def __send_message(self, channel, message: str):
        self.previous_msg.append(await channel.send(message))


# TODO; update 함수 비동기로 바꾸기


class RussianRouletteStarter:
    def __init__(self, user1: disnake.Member, user2: disnake, channel: disnake.TextChannel):
        self.channel = channel
        self.user1 = user1
        self.user2 = user2
        self.true_bullet = 0
        self.total_bullet = 0

    async def start(self):
        msg = await self.channel.send("진짜 총알의 수를 정해주세요")
        OnMessageListener.add_listener(RussianRouletteParamObserver([self.user1, self.user2], msg))
