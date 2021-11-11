import struct


def assert_success(data: dict) -> dict:
    if data.get("code") != 0:
        raise ConnectionError(data["code"], data["message"])
    return data["data"]


class LiveDanmuPacket:
    @staticmethod
    def pack(data: bytes, proto_ver: int, pkg_type: int) -> bytes:
        # 12 bytes header + datq
        return struct.pack("!IHHII", 12, 16, proto_ver, pkg_type, 1) + data

    @staticmethod
    def unpack(data: bytes):
        pass
