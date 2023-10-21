from .header import Header


class Response:
    def __init__(
        self, header: Header, command_code: bytes, response_code: bytes, text: bytes
    ) -> None:
        self.header = header
        self.command_code = command_code
        self.response_code = response_code
        self.text = text

    @property
    def data(self) -> bytes:
        return self.header.data + self.command_code + self.response_code + self.text

    @classmethod
    def from_bytes(cls, data: bytes) -> "Response":
        return cls(
            header=Header.from_bytes(data[:10]),
            command_code=data[10:12],
            response_code=data[12:14],
            text=data[14:],
        )
