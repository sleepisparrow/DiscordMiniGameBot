class Observer:
    async def update(self, **kwargs):
        raise NotImplementedError
