from .base import APIBase, Network


class User(APIBase):
    base = "https://api.bilibili.com/x"

    def __init__(self, network: Network, uid: int):
        super(User, self).__init__(network)
        self.uid = uid

    async def my_info(self) -> dict:
        return await self._get("/space/myinfo")

    async def info(self) -> dict:
        return await self._get("/space/acc/info", {"mid": self.uid})

    async def stat(self) -> dict:
        return await self._get("/relation/stat", {"vmid": self.uid})

    async def upstat(self) -> dict:
        return await self._get("/space/upstat", {"mid": self.uid})

    async def live_info(self) -> dict:
        return await self._get("/space/acc/info", {"mid": self.uid})
