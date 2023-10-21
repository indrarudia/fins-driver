import socket

from .command import Command
from .exceptions import FinsException
from .response import Response


class Client:
    def __init__(
        self, host: str = "127.0.0.1", port: int = 9600, timeout: int = 2000
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.buffer_size = 4096
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, command: Command) -> Response:
        self._socket.send(command.data)
        try:
            data = self._socket.recv(self.buffer_size)
        except FinsException:
            pass
        return data

    def connect(self) -> None:
        self._socket.connect((self.host, self.port))
        self._socket.settimeout(self.timeout)

    def close(self) -> None:
        self._socket.close()

    def __del__(self) -> None:
        self._socket.close()
