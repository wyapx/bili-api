import json
import struct
from typing import Tuple, List, Union, Any


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
    def unpack(data: bytes) -> List[Tuple[Tuple[int, int, int, int, int], Union[dict, bytes]]]:
        if len(data) < 16:
            raise ValueError("not a valid pack")
        offset = 0
        result = []
        while offset != len(data):
            head_offset = offset + 16
            header = struct.unpack("!IHHII", data[offset:head_offset])
            data_len = offset + header[0]
            if data[head_offset] == 123:
                result.append((header, json.loads(data[head_offset:data_len])))
            else:
                result.append((header, data[head_offset:data_len]))
            offset += header[0]
        return result
