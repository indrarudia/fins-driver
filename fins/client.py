import socket
from typing import List, Literal, Union

from .command import (
    MEMORY_AREA_FILL,
    MEMORY_AREA_READ,
    MEMORY_AREA_WRITE,
    MULTIPLE_MEMORY_AREA_READ,
    Command,
)
from .header import Header
from .memory import MemoryAddress
from .response import Response


class FinsClient:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9600,
        timeout: int = 2000,
        mode: Literal["tcp", "udp"] = "udp",
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.buffer_size: int = 4096
        if mode == "udp":
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif mode == "tcp":
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            raise ValueError(f"Unknown client mode: {mode}")

        self.dna: int = 0
        self.da1: int = 0
        self.da2: int = 0
        self.sna: int = 0
        self.sa1: int = 1
        self.sa2: int = 0
        self.sid: int = 0

    def send(self, command: Command) -> bytes:
        self._socket.send(command.bytes)
        data = self._socket.recv(self.buffer_size)
        return Response.from_bytes(data, command)

    def connect(self) -> None:
        self._socket.connect((self.host, self.port))
        self._socket.settimeout(self.timeout)

    def close(self) -> None:
        self._socket.close()

    def __del__(self) -> None:
        self._socket.close()

    def _build_header(self) -> Header:
        return Header(
            icf=b"\x80",
            rsv=b"\x00",
            gct=b"\x07",
            dna=self.dna.to_bytes(1, "big"),
            da1=self.da1.to_bytes(1, "big"),
            da2=self.da2.to_bytes(1, "big"),
            sna=self.sna.to_bytes(1, "big"),
            sa1=self.sa1.to_bytes(1, "big"),
            sa2=self.sa2.to_bytes(1, "big"),
            sid=self.sid.to_bytes(1, "big"),
        )

    def memory_area_read(
        self, address: Union[str, bytes], num_items: int = 1
    ) -> Response:
        addr = MemoryAddress(address)
        cmd = Command(
            code=MEMORY_AREA_READ,
            data=addr.bytes + num_items.to_bytes(2, "big"),
            header=self._build_header(),
        )
        return self.send(cmd)

    def memory_area_write(
        self, address: Union[str, bytes], data: bytes, num_items: int = 1
    ) -> Response:
        addr = MemoryAddress(address)
        cmd = Command(
            code=MEMORY_AREA_WRITE,
            data=addr.bytes + num_items.to_bytes(2, "big") + data,
            header=self._build_header(),
        )
        return self.send(cmd)

    def memory_area_fill(
        self, address: Union[str, bytes], data: bytes, num_items: int = 1
    ) -> Response:
        addr = MemoryAddress(address)
        cmd = Command(
            code=MEMORY_AREA_FILL,
            data=addr.bytes + num_items.to_bytes(2, "big") + data,
            header=self._build_header(),
        )
        return self.send(cmd)

    def multiple_memory_area_read(
        self, *addresses: List[Union[str, bytes]]
    ) -> Response:
        data = []
        for address in addresses:
            addr = MemoryAddress(address)
            data.append(addr.bytes)

        cmd = Command(
            code=MULTIPLE_MEMORY_AREA_READ,
            data=b"".join(data),
            header=self._build_header(),
        )
        return self.send(cmd)
