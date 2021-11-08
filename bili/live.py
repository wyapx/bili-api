from .base import APIBase


class Live(APIBase):
    base = "https://api.live.bilibili.com"

    async def _get_live(self, room_id: int, call_api: str, need_verify=False) -> dict:
        return await self.get("/xlive/web-room/v1/index/" + call_api, {"room_id": room_id})

    async def user_info_in_room(self, room_id: int) -> dict:
        return await self._get_live(room_id, "getInfoByUser", True)

    async def room_info(self, room_id: int) -> dict:
        return await self._get_live(room_id, "getInfoByRoom")

    async def room_play_info(self, room_id: int) -> dict:
        return await self._get_live(room_id, "getRoomPlayInfo")

    async def chat_conf(self, room_id: int) -> dict:
        return await self.get("/room/v1/Danmu/getConf", {"room_id": room_id})
