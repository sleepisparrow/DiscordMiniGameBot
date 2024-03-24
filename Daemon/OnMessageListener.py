from Daemon.Observer import Observer


class OnMessageListener:
    __target_list = []

    @classmethod
    def add_listener(cls, target: Observer):
        cls.__target_list.append(target)

    @classmethod
    def remove_observer(cls, target: Observer):
        cls.__target_list.remove(target)

    @classmethod
    async def alert(cls, message):
        for observer in cls.__target_list:
            await observer.update(message)
