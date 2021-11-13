import asyncio
import json
import brotli
import aiohttp

from .base import APIBase, Network
from .utils import LiveDanmuPacket


class Live(APIBase):
    base = "https://api.live.bilibili.com"

    def __init__(self, network: Network, room_id: int):
        super(Live, self).__init__(network)
        self.room_id = room_id

    async def _get_live(self, call_api: str, api_version=1) -> dict:
        return await self._get(f"/xlive/web-room/v{api_version}/index/{call_api}", {"room_id": self.room_id})

    async def user_info_in_room(self) -> dict:
        await self.verify_auth()
        return await self._get_live("getInfoByUser")

    async def room_info(self) -> dict:
        return await self._get_live("getInfoByRoom")

    async def room_play_info(self) -> dict:
        return await self._get_live("getRoomPlayInfo")

    async def chat_conf(self) -> dict:
        return await self._get("/room/v1/Danmu/getConf", {"room_id": self.room_id})


class LiveDanmu:
    def __init__(self, network: Network, live: Live, *, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()
        self._network = network
        self._ws: aiohttp.ClientWebSocketResponse = ...
        self._loop = loop
        self.live = live

    async def _send_bytes(self, data: bytes, proto_ver: int, pkg_type: int):
        await self._ws.send_bytes(
            LiveDanmuPacket.pack(data, proto_ver, pkg_type)
        )

    async def _send_json(self, data: dict, proto_ver: int, pkg_type: int):
        return await self._send_bytes(json.dumps(data).encode(), proto_ver, pkg_type)

    async def _verify(self, token: str):
        await self._send_json({
            "uid": 0,
            "roomid": self.live.room_id,
            "protover": 3,
            "type": 2,
            "platform": "web",
            "token": token
        }, 1, 7)

    async def __heartbeat(self):
        while not self._ws.closed:
            await self._send_bytes(b"", 1, 2)
            await asyncio.sleep(10)

    async def connect(self):
        if isinstance(self._ws, aiohttp.ClientWebSocketResponse):
            raise ConnectionResetError('websocket connection already open')
        # await self.live.verify_auth()
        conf = await self.live.chat_conf()
        self._ws = await self._network.websocket(conf["host"], "/sub", port=443)
        await self._verify(conf["token"])
        self._loop.create_task(self.__heartbeat())
        while not self._ws.closed:
            raw = await self._ws.receive()
            if raw.type == 257:
                break
            elif raw.type == 2:
                for header, data in LiveDanmuPacket.unpack(raw.data):
                    if header[2] == 3:
                        print(LiveDanmuPacket.unpack(brotli.decompress(data)))
                    else:
                        print(header, data)
