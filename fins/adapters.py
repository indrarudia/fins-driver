import io
from typing import List

from .memory import MemoryArea


class BaseDataAdapter:
    def __call__(self, data: bytes) -> bytes:
        return data


class MultipleMemoryAreaReadDataAdapter(BaseDataAdapter):
    def __init__(self, addresses: List[MemoryArea]) -> None:
        super().__init__()
        self.addresses = addresses

    def __call__(self, data: bytes) -> List[bytes]:
        values: List[bytes] = []
        buf = io.BytesIO(data)
        for addr in self.addresses:
            buf.read(1)  # Read memory area code.
            if addr.is_bit_set():
                d = buf.read(1)
            else:
                d = buf.read(2)
            values.append(d)
        return values
