from typing import Union


class Header:
    def __init__(
        self,
        icf: bytes,
        rsv: bytes,
        gct: bytes,
        dna: bytes,
        da1: bytes,
        da2: bytes,
        sna: bytes,
        sa1: bytes,
        sa2: bytes,
        sid: bytes,
    ) -> None:
        self.icf = icf
        self.rsv = rsv
        self.gct = gct
        self.dna = dna
        self.da1 = da1
        self.da2 = da2
        self.sna = sna
        self.sa1 = sa1
        self.sa2 = sa2
        self.sid = sid

    @property
    def data(self) -> bytes:
        return (
            self.icf
            + self.rsv
            + self.gct
            + self.dna
            + self.da1
            + self.da2
            + self.sna
            + self.sa1
            + self.sa2
            + self.sid
        )

    def __add__(self, other: Union["Header", bytes]) -> bytes:
        if isinstance(other, Header):
            return self.data + other.data
        elif isinstance(other, bytes):
            return self.data + other
        else:
            raise TypeError(f"Unsupported type: {type(other)}")


def default_request_header() -> Header:
    return Header(
        icf=b"\x80",
        rsv=b"\x00",
        gct=b"\x02",
        dna=b"\x00",
        da1=b"\x00",
        da2=b"\x00",
        sna=b"\x00",
        sa1=b"\x22",
        sa2=b"\x00",
        sid=b"\x00",
    )
