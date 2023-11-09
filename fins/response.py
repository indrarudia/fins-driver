from functools import cached_property
from typing import Generic, Optional, TypeVar

from .command import Command
from .header import Header
from .response_codes import RESPONSE_CODES

T = TypeVar("T")


class Response(Generic[T]):
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
        adapter: Optional[callable] = None,
    ) -> None:
        self._header = header
        self._command_code = command_code
        self._code = code
        self._command = command
        self._data = data
        self._adapter = adapter

    @property
    def header(self) -> Header:
        return self._header

    @property
    def command_code(self) -> bytes:
        return self._command_code

    @property
    def code(self) -> bytes:
        return self._code

    @property
    def command(self) -> Command:
        return self._command

    @property
    def raw_data(self) -> bytes:
        return self._data

    @cached_property
    def data(self) -> T:
        """
        Returns a friendly data format that has been transformed by adapter
        function.
        """
        if self._adapter is None:
            return self.raw_data
        if not self.ok:
            return b""
        return self._adapter(self.raw_data)

    @property
    def raw(self) -> bytes:
        """Returns the raw content of the response, in bytes."""
        return self.header.raw + self.command_code + self.code + self.raw_data

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
        return "Unknown"

    def __repr__(self) -> str:
        return "<FINS Response: {}>".format(self.code)

    def __str__(self) -> str:
        return str(self.raw)
