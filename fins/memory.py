import re
from dataclasses import dataclass
from typing import Optional, Tuple, Union


class MemoryAreaCode:
    CIO_BIT = b"\x30"
    WORK_BIT = b"\x31"
    HOLDING_BIT = b"\x32"
    AUXILIARY_BIT = b"\x33"
    CIO_BIT_FORCED = b"\70"
    WORK_BIT_FORCED = b"\x71"
    HOLDING_BIT_FORCED = b"\x72"
    CIO_WORD = b"\xB0"
    WORK_WORD = b"\xB1"
    HOLDING_WORD = b"\xB2"
    AUXILIARY_WORD = b"\xB3"
    CIO_WORD_FORCED = b"\xF0"
    WORK_WORD_FORCED = b"\xF1"
    HOLDING_WORD_FORCED = b"\xF2"
    TIMER_FLAG = b"\x09"
    COUNTER_FLAG = b"\x09"
    TIMER_FLAG_FORCED = b"\x49"
    COUNTER_FLAG_FORCED = b"\x49"
    TIMER_WORD = b"\x89"
    COUNTER_WORD = b"\x89"
    DATA_MEMORY_BIT = b"\x02"
    DATA_MEMORY_WORD = b"\x82"
    EM0_BIT = b"\x20"
    EM1_BIT = b"\x21"
    EM2_BIT = b"\x22"
    EM3_BIT = b"\x23"
    EM4_BIT = b"\x24"
    EM5_BIT = b"\x25"
    EM6_BIT = b"\x26"
    EM7_BIT = b"\x27"
    EM8_BIT = b"\x28"
    EM9_BIT = b"\x29"
    EMA_BIT = b"\x2A"
    EMB_BIT = b"\x2B"
    EMC_BIT = b"\x2C"
    EMD_BIT = b"\x2D"
    EME_BIT = b"\x2E"
    EMF_BIT = b"\x2F"
    EM10_BIT = b"\xE0"
    EM11_BIT = b"\xE1"
    EM12_BIT = b"\xE2"
    EM13_BIT = b"\xE3"
    EM14_BIT = b"\xE4"
    EM15_BIT = b"\xE5"
    EM16_BIT = b"\xE6"
    EM17_BIT = b"\xE7"
    EM18_BIT = b"\xE8"
    EM0_WORD = b"\xA0"
    EM1_WORD = b"\xA1"
    EM2_WORD = b"\xA2"
    EM3_WORD = b"\xA3"
    EM4_WORD = b"\xA4"
    EM5_WORD = b"\xA5"
    EM6_WORD = b"\xA6"
    EM7_WORD = b"\xA7"
    EM8_WORD = b"\xA8"
    EM9_WORD = b"\xA9"
    EMA_WORD = b"\xAA"
    EMB_WORD = b"\xAB"
    EMC_WORD = b"\xAC"
    EMD_WORD = b"\xAD"
    EME_WORD = b"\xAE"
    EMF_WORD = b"\xAF"
    EM10_WORD = b"\x60"
    EM11_WORD = b"\x61"
    EM12_WORD = b"\x62"
    EM13_WORD = b"\x63"
    EM14_WORD = b"\x64"
    EM15_WORD = b"\x65"
    EM16_WORD = b"\x66"
    EM17_WORD = b"\x67"
    EM18_WORD = b"\x68"
    EM_CURR_BANK_BIT = b"\x0A"
    EM_CURR_BANK_WORD = b"\x98"
    EM_CURR_BANK_NUMBER = b"\xBC"
    TASK_FLAG_BIT = b"\x06"
    TASK_FLAG_STATUS = b"\x46"
    INDEX_REGISTER = b"\xDC"
    DATA_REGISTER = b"\xBC"
    CLOCK_PULSES = b"\x07"
    CONDITION_FLAGS = b"\x07"


@dataclass
class AddressSet:
    word: bytes
    bit: Optional[bytes] = None
    word_forced: Optional[bytes] = None
    bit_forced: Optional[bytes] = None


MEMORY_AREAS_PREFIX = {
    "CIO": AddressSet(
        word=MemoryAreaCode.CIO_WORD,
        bit=MemoryAreaCode.CIO_BIT,
        word_forced=MemoryAreaCode.CIO_WORD_FORCED,
        bit_forced=MemoryAreaCode.CIO_BIT_FORCED,
    ),
    "W": AddressSet(
        word=MemoryAreaCode.WORK_WORD,
        bit=MemoryAreaCode.WORK_BIT,
        word_forced=MemoryAreaCode.WORK_WORD_FORCED,
        bit_forced=MemoryAreaCode.WORK_BIT_FORCED,
    ),
    "H": AddressSet(
        word=MemoryAreaCode.HOLDING_WORD,
        bit=MemoryAreaCode.HOLDING_BIT,
        word_forced=MemoryAreaCode.HOLDING_WORD_FORCED,
        bit_forced=MemoryAreaCode.HOLDING_BIT_FORCED,
    ),
    "A": AddressSet(
        word=MemoryAreaCode.AUXILIARY_WORD,
        bit=MemoryAreaCode.AUXILIARY_BIT,
    ),
    "D": AddressSet(
        word=MemoryAreaCode.DATA_MEMORY_WORD,
        bit=MemoryAreaCode.DATA_MEMORY_BIT,
    ),
}


class MemoryArea:
    """
    A class to encapsulate memory address.

    It can be used to translate memory address from string, e.g CIO100.1, D0,
    W22, etc to bytes representation. For example:

        CIO100.1 -> b"\xb0\x00\x64\x01"

    If input value is already in bytes, parse the matching area code, word, and
    its bit.
    """

    def __init__(self, value: Union[str, bytes]) -> None:
        if isinstance(value, str):
            area, word, bit = self._parse_addr_string(value)
        elif isinstance(value, bytes):
            area, word, bit = self._parse_addr_bytes(value)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

        self.area: bytes = area
        self.word: bytes = word
        self.bit: bytes = bit

    def _parse_addr_string(self, value: str) -> Tuple[bytes, bytes, bytes]:
        regex = re.compile("(?P<area>[A-Z]+)?(?P<word>\d+)(\.(?P<bit>\d+))?")
        match = regex.match(value)
        if match:
            area = match.groupdict()["area"]
            address = match.groupdict()["word"]
            bit = match.groupdict()["bit"]
        else:
            raise ValueError("Invalid memory address format")
        if area is not None and area not in MEMORY_AREAS_PREFIX:
            raise ValueError(f"Unsupported memory area: {area}")

        if bit is None:
            bit = b"\x00"
            if area in MEMORY_AREAS_PREFIX:
                area = MEMORY_AREAS_PREFIX[area].word
            else:
                area = MemoryAreaCode.CIO_WORD
        else:
            bit = int(bit).to_bytes(1, "big")
            if area in MEMORY_AREAS_PREFIX:
                area = MEMORY_AREAS_PREFIX[area].bit
            else:
                area = MemoryAreaCode.CIO_BIT

        word = int(address).to_bytes(2, "big")
        return area, word, bit

    def _parse_addr_bytes(self, value: bytes) -> Tuple[bytes, bytes, bytes]:
        if len(value) != 4:
            raise ValueError("Insufficient address bytes length")
        area = value[0:1]
        word = value[1:3]
        bit = value[3:5]
        return area, word, bit

    @property
    def raw(self) -> bytes:
        """Returns the raw content of the memory, in bytes."""
        return self.area + self.word + self.bit

    def __repr__(self) -> str:
        return "<MemoryArea: {}>".format(self.raw)

    def __str__(self) -> str:
        value = {"area": self.area, "word": self.word, "bit": self.bit}
        return str(value)
