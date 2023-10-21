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
        return self.header + self.command_code + self.response_code + self.text
