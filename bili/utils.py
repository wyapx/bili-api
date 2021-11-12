import struct


def assert_success(data: dict) -> dict:
    if data.get("code") != 0:
        raise ConnectionError(data["code"], data["message"])
    return data["data"]


class LiveDanmuPacket:
    @staticmethod
    def pack(data: bytes, proto_ver: int, pkg_type: int) -> bytes:
        # 16 bytes header + data
        return struct.pack("!IHHII", 16 + len(data), 16, proto_ver, pkg_type, 1) + data

    @staticmethod
    def unpack(data: bytes):
        if len(data) < 16:
            raise ValueError("not a valid pack")
        return struct.unpack("!IHHII", data[:16]), data[16:]
