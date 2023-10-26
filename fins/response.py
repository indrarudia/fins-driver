from .header import Header


class Response:
    def __init__(
        self,
        header: Header,
        command_code: bytes,
        code: bytes,
        data: bytes,
    ) -> None:
        self.header = header
        self.command_code = command_code
        self.code = code
        self.data = data

    @property
    def bytes(self) -> bytes:
        return self.header.data + self.command_code + self.code + self.data

    @classmethod
    def from_bytes(cls, data: bytes) -> "Response":
        return cls(
            header=Header.from_bytes(data[:10]),
            command_code=data[10:12],
            code=data[12:14],
            data=data[14:],
        )
