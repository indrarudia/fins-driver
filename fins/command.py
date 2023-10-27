from typing import Union, Optional

from .header import Header
from .memory import MemoryArea


class CommandCode:
    MEMORY_AREA_READ = b"\x01\x01"
    MEMORY_AREA_WRITE = b"\x01\x02"
    MEMORY_AREA_FILL = b"\x01\x03"
    MULTIPLE_MEMORY_AREA_READ = b"\x01\x04"
    MEMORY_AREA_TRANSFER = b"\x01\x05"
    PARAMETER_AREA_READ = b"\x02\x01"
    PARAMETER_AREA_WRITE = b"\x02\x02"
    PARAMETER_AREA_CLEAR = b"\x02\x03"
    DATA_LINK_TABLE_READ = b"\x02\x20"
    DATA_LINK_TABLE_WRITE = b"\x02\x21"
    PROGRAM_AREA_PROTECT = b"\x03\04"
    PROGRAM_AREA_PROTECT_CLEAR = b"\x03\x05"
    PROGRAM_AREA_READ = b"\x03\x06"
    PROGRAM_AREA_WRITE = b"\x03\x07"
    PROGRAM_AREA_CLEAR = b"\x03\x08"
    RUN = b"\x04\x01"
    STOP = b"\x04\x02"
    RESET = b"\x04\03"
    CONTROLLER_DATA_READ = b"\x05\x01"
    CONNECTION_DATA_READ = b"\x05\x02"
    CONTROLLER_STATUS_READ = b"\x06\x01"
    NETWORK_STATUS_READ = b"\x06\x02"
    CYCLE_TIME_READ = b"\x06\x20"
    CLOCK_READ = b"\x07\x01"
    CLOCK_WRITE = b"\x07\x02"
    MESSAGE_READ = b"\x09\x20"
    MESSAGE_CLEAR = b"\x09\x20"
    FAL_FALS_READ = b"\x09\x20"
    ACCESS_RIGHT_ACQUIRE = b"\x0C\x01"
    ACCESS_RIGHT_FORCED_ACQUIRE = b"\x0C\x02"
    ACCESS_RIGHT_RELEASE = b"\x0C\x03"
    ERROR_CLEAR = b"\x21\x01"
    ERROR_LOG_READ = b"\x21\x02"
    ERROR_LOG_CLEAR = b"\x21\x03"
    FILE_NAME_READ = b"\x22\x01"
    SINGLE_FILE_READ = b"\x22\x02"
    SINGLE_FILE_WRITE = b"\x22\x03"
    MEMORY_CARD_FORMAT = b"\x22\x04"
    FILE_DELETE = b"\x22\x05"
    VOLUME_LABEL_CREATE_DELETE = b"\x22\x06"
    FILE_COPY = b"\x22\x07"
    FILE_NAME_CHANGE = b"\x22\x08"
    MEMORY_AREA_FILE_TRANSFER = b"\x22\x0A"
    PARAMETER_AREA_FILE_TRANSFER = b"\x22\x0B"
    PROGRAM_AREA_FILE_TRANSFER = b"\x22\x0C"
    FORCED_SET_RESET = b"\x23\x01"
    FORCED_SET_RESET_CANCEL = b"\x23\x02"


class Command:
    """
    A class to encapsulate FINS command.
    """

    def __init__(
        self, code: bytes, data: bytes = b"", header: Optional[Header] = None
    ) -> None:
        if header is None:
            header = Header.default()

        #: Command header.
        self.header = header

        #: Command code, in bytes.
        self.code = code

        #: Command data, in bytes.
        self.data = data

    @property
    def raw(self) -> bytes:
        """Returns the content of the command, in bytes."""
        return self.header.raw + self.code + self.data

    def __repr__(self) -> str:
        return "<FINS Command: {}>".format(self.code)

    def __str__(self) -> str:
        return str(self.raw)


class SetResetSpecCode:
    FORCE_RESET = b"\x00\x00"
    FORCE_SET = b"\x00\x01"
    FORCED_RELEASED_BIT_OFF = b"\x80\x00"
    FORCED_RELEASED_BIT_ON = b"\x80\x01"
    FORCED_RELEASED = b"\xff\xff"


class SetResetSpec:
    """
    Class to store Forced set/reset specification data.
    """

    def __init__(self, spec: bytes, address: Union[str, bytes]) -> None:
        #: Set/Reset specification code, in bytes.
        self.spec = spec

        #: Memory address area.
        self.address = address

    @property
    def raw(self) -> bytes:
        """Returns the raw content of set/reset specification in bytes."""
        return self.spec + MemoryArea(self.address).raw
