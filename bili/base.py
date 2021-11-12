from typing import Dict

import aiohttp

from .utils import assert_success


class Network:
    def __init__(self, cookies: Dict[str, str] = None) -> None:
        cookiejar = aiohttp.CookieJar()
        if cookies:
            cookiejar.update_cookies(cookies)
        self._session = aiohttp.ClientSession(cookie_jar=cookiejar)

    async def get(self, url: str, params=None) -> dict:
        async with self._session.get(url, params=params) as resp:
            if resp.status != 200:
                raise ConnectionError(resp.status, await resp.read())
            return await resp.json()

    async def post(self, url: str, data=None) -> dict:
        async with self._session.post(url, data=data) as resp:
            if resp.status != 200:
                raise ConnectionError(resp.status, await resp.read())
            return await resp.json()

    async def websocket(self, host: str, path="/", port=443, wss=True) -> aiohttp.ClientWebSocketResponse:
        return await self._session.ws_connect(f"{'wss' if wss else 'ws'}://"
                                              f"{host}:{port}{path}")


class APIBase:
    base = None

    def __init__(self, network: Network) -> None:
        if not self.base:
            raise AttributeError("base url not set")
        self._network = network
        self._verified = None

    def _join_url(self, path: str) -> str:
        return self.base + path

    async def verify_auth(self):
        if self._verified is None:
            assert_success(
                await self._network.get("https://api.bilibili.com/x/space/myinfo")
            )
            self._verified = True

    async def _get(self, path: str, params=None) -> dict:
        return assert_success(
            await self._network.get(self._join_url(path), params)
        )

    async def _post(self, path: str, data=None) -> dict:
        return assert_success(
            await self._network.post(self._join_url(path), data)
        )
