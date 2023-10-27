from typing import Optional, Union

from .header import Header, default_header
from .memory import MemoryAddress

MEMORY_AREA_READ = b"\x01\x01"
MEMORY_AREA_WRITE = b"\x01\x02"
MEMORY_AREA_FILL = b"\x01\x03"
MULTIPLE_MEMORY_AREA_READ = b"\x01\x04"
MEMORY_AREA_TRANSFER = b"\x01\x05"
PARAMETER_AREA_READ = b"\x02\x01"
PARAMETER_AREA_WRITE = b"\x02\x02"
PARAMETER_AREA_FILL = b"\x02\x03"
PROGRAM_AREA_READ = b"\x03\x06"
PROGRAM_AREA_WRITE = b"\x03\x07"
PROGRAM_AREA_CLEAR = b"\x03\x08"
RUN = b"\x04\x01"
STOP = b"\x04\x02"
CPU_UNIT_DATA_READ = b"\x05\x01"
CONNECTION_DATA_READ = b"\x05\x02"
CPU_UNIT_STATUS_READ = b"\x06\x01"
CYCLE_TIME_READ = b"\x06\x20"
CLOCK_READ = b"\x07\x01"
CLOCK_WRITE = b"\x07\x02"
MESSAGE_READ = b"\x09\x20"
ACCESS_RIGHT_ACQUIRE = b"\x0C\x01"
ACCESS_RIGHT_FORCED_ACQUIRE = b"\x0C\x02"
ACCESS_RIGHT_RELEASE = b"\x0C\x03"
ERROR_CLEAR = b"\x21\x01"
ERROR_LOG_READ = b"\x21\x02"
ERROR_LOG_CLEAR = b"\x21\x03"
FINS_WRITE_ACCESS_LOG_READ = b"\x21\x40"
FINS_WRITE_ACCESS_LOG_CLEAR = b"\x21\x41"
FILE_NAME_READ = b"\x22\x01"
SINGLE_FILE_READ = b"\x22\x02"
SINGLE_FILE_WRITE = b"\x22\x03"
FILE_MEMORY_FORMAT = b"\x22\x04"
FILE_DELETE = b"\x22\x05"
FILE_COPY = b"\x22\x07"
FILE_NAME_CHANGE = b"\x22\x08"
MEMORY_AREA_FILE_TRANSFER = b"\x22\x0A"
PARAMETER_AREA_FILE_TRANSFER = b"\x22\x0B"
PROGRAM_AREA_FILE_TRANSFER = b"\x22\x0C"
DIRECTORY_CREATE_DELETE = b"\x22\x15"
MEMORY_CASSETTE_TRANSFER = b"\x22\x20"
FORCED_SET_RESET = b"\x23\x01"
FORCED_SET_RESET_CANCEL = b"\x23\x02"
CONVERT_TO_COMPOWAY_F_COMMAND = b"\x28\x03"
CONVERT_TO_MODBUS_RTU_COMMAND = b"\x28\x04"
CONVERT_TO_MODBUS_ASCII_COMMAND = b"\x28\x05"


class Command:
    def __init__(
        self, code: bytes, data: bytes = b"", header: Optional[Header] = None
    ) -> None:
        if header is None:
            self.header = default_header()
        else:
            self.header = header
        self.code = code
        self.data = data

    @property
    def bytes(self) -> bytes:
        return self.header.bytes + self.code + self.data

    def to_bytes(self) -> bytes:
        return self.bytes


FORCE_RESET = b"\x00\x00"
FORCE_SET = b"\x00\x01"
FORCED_RELEASED_BIT_OFF = b"\x80\x00"
FORCED_RELEASED_BIT_ON = b"\x80\x01"
FORCED_RELEASED = b"\xff\xff"


class SetResetSpec:
    def __init__(self, spec: bytes, address: Union[str, bytes]) -> None:
        self.spec = spec
        self.address = address

    def to_bytes(self) -> bytes:
        return self.spec + MemoryAddress(self.address).to_bytes()
