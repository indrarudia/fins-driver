import socket
from typing import Literal, Union

from .command import Command, CommandCode, SetResetSpec
from .header import Header
from .memory import MemoryArea
from .response import Response


class FinsClient:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9600,
        timeout: int = 5,
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
        self._socket.settimeout(self.timeout)

        self.dna: int = 0
        self.da1: int = 0
        self.da2: int = 0
        self.sna: int = 0
        self.sa1: int = 1
        self.sa2: int = 0
        self.sid: int = 0

    def send(self, command: Command) -> bytes:
        self._socket.send(command.raw)
        data = self._socket.recv(self.buffer_size)
        return Response(
            header=Header.from_bytes(data[:10]),
            command_code=data[10:12],
            code=data[12:14],
            data=data[14:],
            command=command,
        )

    def connect(self) -> None:
        self._socket.connect((self.host, self.port))

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
        addr = MemoryArea(address)
        cmd = Command(
            code=CommandCode.MEMORY_AREA_READ,
            data=addr.raw + num_items.to_bytes(2, "big"),
            header=self._build_header(),
        )
        return self.send(cmd)

    def memory_area_write(
        self, address: Union[str, bytes], data: bytes, num_items: int = 1
    ) -> Response:
        addr = MemoryArea(address)
        cmd = Command(
            code=CommandCode.MEMORY_AREA_WRITE,
            data=addr.raw + num_items.to_bytes(2, "big") + data,
            header=self._build_header(),
        )
        return self.send(cmd)

    def memory_area_fill(
        self, address: Union[str, bytes], data: bytes, num_items: int = 1
    ) -> Response:
        addr = MemoryArea(address)
        cmd = Command(
            code=MemoryArea.MEMORY_AREA_FILL,
            data=addr.raw + num_items.to_bytes(2, "big") + data,
            header=self._build_header(),
        )
        return self.send(cmd)

    def multiple_memory_area_read(self, *addresses: Union[str, bytes]) -> Response:
        data = []
        for address in addresses:
            addr = MemoryArea(address)
            data.append(addr.raw)

        cmd = Command(
            code=CommandCode.MULTIPLE_MEMORY_AREA_READ,
            data=b"".join(data),
            header=self._build_header(),
        )
        return self.send(cmd)

    def memory_area_transfer(
        self,
        source_address: Union[str, bytes],
        dest_address: Union[str, bytes],
        num_items: int = 1,
    ) -> Response:
        src_addr = MemoryArea(source_address)
        dest_addr = MemoryArea(dest_address)
        cmd = Command(
            code=CommandCode.MEMORY_AREA_TRANSFER,
            data=src_addr.raw + dest_addr.raw + num_items.to_bytes(2, "big"),
            header=self._build_header(),
        )
        return self.send(cmd)

    def run(
        self,
        mode: Literal["debug", "monitor", "run"] = "monitor",
        program_number: bytes = b"\xff\xff",
    ) -> Response:
        modes = {"debug": b"\x01", "monitor": b"\x02", "run": b"\x04"}
        cmd = Command(
            code=CommandCode.RUN,
            data=program_number + modes[mode],
            header=self._build_header(),
        )
        return self.send(cmd)

    def stop(self) -> Response:
        cmd = Command(
            code=CommandCode.STOP,
            header=self._build_header(),
        )
        return self.send(cmd)

    def forced_set_reset(self, *specs: SetResetSpec) -> Response:
        data = []
        for spec in specs:
            data.append(spec.raw)
        num_items = len(data)
        cmd = Command(
            code=CommandCode.FORCED_SET_RESET,
            data=num_items.to_bytes(2, "big") + b"".join(data),
            header=self._build_header(),
        )
        return self.send(cmd)

    def forced_set_reset_cancel(self) -> Response:
        cmd = Command(
            code=CommandCode.FORCED_SET_RESET_CANCEL,
            header=self._build_header(),
        )
        return self.send(cmd)
