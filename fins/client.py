import socket
from typing import Literal

from .command import Command
from .response import Response


class Client:
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

    def send(self, command: Command) -> Response:
        self._socket.send(command.data)
        data = self._socket.recv(self.buffer_size)
        return Response.from_bytes(data)

    def connect(self) -> None:
        self._socket.connect((self.host, self.port))
        self._socket.settimeout(self.timeout)

    def close(self) -> None:
        self._socket.close()

    def __del__(self) -> None:
        self._socket.close()
