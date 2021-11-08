from .base import APIBase


class User(APIBase):
    base = "https://api.bilibili.com/x"

    async def my_info(self) -> dict:
        url = "/space/myinfo"
        return await self.get(url)

    async def info(self, uid: int) -> dict:
        url = "/space/acc/info"
        return await self.get(url, {"mid": uid})

    async def stat(self, uid: int) -> dict:
        url = "/relation/stat"
        return await self.get(url, {"vmid": uid})

    async def upstat(self, uid: int) -> dict:
        url = "/space/upstat"
        return await self.get(url, {"mid": uid})

    async def live_info(self, uid: int) -> dict:
        url = "/space/acc/info"
        return await self.get(url, {"mid": uid})