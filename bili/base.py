import aiohttp


class Network:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    def get(self, url: str, data=None) -> dict:
        pass

    def post(url: str, data=None) -> dict:
        pass



class APIBase:
    def __init__(self) -> None:
        pass