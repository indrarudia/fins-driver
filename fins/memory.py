import binascii
import re
from dataclasses import dataclass
from typing import Optional, Union

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


MEMORY_AREAS = {
    "CIO": AddressSet(
        word=CIO_WORD,
        bit=CIO_BIT,
        word_forced=CIO_WORD_FORCED,
        bit_forced=CIO_BIT_FORCED,
    ),
    "W": AddressSet(
        word=WORK_WORD,
        bit=WORK_BIT,
        word_forced=WORK_WORD_FORCED,
        bit_forced=WORK_BIT_FORCED,
    ),
    "H": AddressSet(
        word=HOLDING_WORD,
        bit=HOLDING_BIT,
        word_forced=HOLDING_WORD_FORCED,
        bit_forced=HOLDING_BIT_FORCED,
    ),
    "A": AddressSet(word=AUXILIARY_WORD, bit=AUXILIARY_BIT),
    "D": AddressSet(word=DATA_MEMORY_WORD, bit=DATA_MEMORY_BIT),
    "T": AddressSet(word=TIMER_WORD),
    "C": AddressSet(word=COUNTER_WORD),
    "IR": AddressSet(word=INDEX_REGISTER),
    "DR": AddressSet(word=DATA_REGISTER),
    "TK": AddressSet(word=TASK_FLAG_STATUS, bit=TASK_FLAG_BIT),
}


class MemoryAddress:
    def __init__(self, value: Union[str, bytes]):
        if isinstance(value, str):
            regex = re.compile("(?P<area>[A-Z]+)?(?P<word>\d+)(\.(?P<bit>\d+))?")
            match = regex.match(value)
            if match:
                area = match.groupdict()["area"]
                address = match.groupdict()["word"]
                bit = match.groupdict()["bit"]
            else:
                raise ValueError("Invalid memory address format")

            if bit is None:
                self.bit = b"\x00"
                if area in MEMORY_AREAS:
                    self.area = MEMORY_AREAS[area].word
                else:
                    self.area = CIO_WORD
            else:
                self.bit = int(bit).to_bytes(1, "big")
                if area in MEMORY_AREAS:
                    self.area = MEMORY_AREAS[area].bit
                else:
                    self.area = CIO_BIT

            self.word = int(address).to_bytes(2, "big")

        elif isinstance(value, bytes):
            self.area = value[0:1]
            self.word = value[1:3]
            self.bit = value[3:]

        else:
            raise TypeError(f"Unsupported type: {type(value)}")

        self._value = value

    @property
    def bytes(self) -> bytes:
        return self.area + self.word + self.bit

    def to_bytes(self) -> bytes:
        return self.bytes

    def is_bit_set(self) -> bool:
        return self.bit is not None

    def __str__(self) -> str:
        if isinstance(self._value, str):
            value = "{text} ({hex})".format(
                text=self._value,
                hex=binascii.hexlify(self.bytes, sep=b" ", bytes_per_sep=1),
            )
        else:
            value = "{}".format(binascii.hexlify(self.bytes, sep=b" ", bytes_per_sep=1))
        return value
