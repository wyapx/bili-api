from .base import APIBase, Network


class Live(APIBase):
    base = "https://api.live.bilibili.com"

    def __init__(self, network: Network, room_id: int):
        super(Live, self).__init__(network)
        self.room_id = room_id

    async def _get_live(self, call_api: str, api_version=1) -> dict:
        return await self._get(f"/xlive/web-room/v{api_version}/index/{call_api}", {"room_id": self.room_id})

    async def user_info_in_room(self) -> dict:
        return await self._get_live("getInfoByUser")

    async def room_info(self) -> dict:
        return await self._get_live("getInfoByRoom")

    async def room_play_info(self) -> dict:
        return await self._get_live("getRoomPlayInfo")

    async def chat_conf(self) -> dict:
        return await self._get("/room/v1/Danmu/getConf", {"room_id": self.room_id})
