from .command import Command
from .header import Header
from .response_codes import RESPONSE_CODES


class Response:
    """
    The :class:`Response <Response>` object, which contains a FINS's response to
    a request.
    """

    def __init__(
        self,
        header: Header,
        command_code: bytes,
        code: bytes,
        data: bytes,
        command: Command,
    ) -> None:
        #: Response header.
        self.header = header

        #: Command code, in bytes.
        self.command_code = command_code

        #: Response code, in bytes.
        self.code = code

        #: Response data, in bytes.
        self.data = data

        #: The request command.
        self.command = command

    @property
    def raw(self) -> bytes:
        """Returns the raw content of the response, in bytes."""
        return self.header.raw + self.command_code + self.code + self.data

    @property
    def ok(self) -> bool:
        """
        Returns True if :attr:`status_code` is 0x0000 (Normal completion).
        """
        return self.code == b"\x00\x00"

    @property
    def status_text(self) -> str:
        """
        Returns the human readible text of the status code.
        """
        if self.code in RESPONSE_CODES:
            return RESPONSE_CODES[self.code]
        return "Unknown response code"

    def __repr__(self) -> str:
        return "<FINS Response: {}>".format(self.code)

    def __str__(self) -> str:
        return str(self.raw)
