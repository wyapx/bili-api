import aiohttp


class Network:
    def __init__(self, cookies=None) -> None:
        cookiejar = aiohttp.CookieJar()
        if cookies:
            cookiejar.update_cookies(cookies)
        self._session = aiohttp.ClientSession(cookie_jar=cookiejar)

    async def get(self, url: str, params=None) -> dict:
        async with self._session.get(url, body=params) as resp:
            if resp.status != 200:
                raise ConnectionError(resp.status, await resp.read())
            return await resp.json()

    async def post(self, url: str, data=None) -> dict:
        async with self._session.post(url, data=data) as resp:
            if resp.status != 200:
                raise ConnectionError(resp.status, await resp.read())
            return await resp.json()


class APIBase:
    def __init__(self, network: Network) -> None:
        self._network = network
