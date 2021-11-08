from .base import APIBase


class User(APIBase):
    base = "https://api.bilibili.com/x"

    async def my_info(self) -> dict:
        return await self.get("/space/myinfo")

    async def info(self, uid: int) -> dict:
        return await self.get("/space/acc/info", {"mid": uid})

    async def stat(self, uid: int) -> dict:
        return await self.get("/relation/stat", {"vmid": uid})

    async def upstat(self, uid: int) -> dict:
        return await self.get("/space/upstat", {"mid": uid})

    async def live_info(self, uid: int) -> dict:
        return await self.get("/space/acc/info", {"mid": uid})
