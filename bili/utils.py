def assert_success(data: dict) -> dict:
    if data.get("code") != 0:
        raise ConnectionError(data["code"], data["msg"])
    return data["data"]
