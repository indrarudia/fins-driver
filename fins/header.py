from typing import Iterator


class Header:
    """
    FINS header class.
    """

    __attrs__ = ["icf", "rsv", "gct", "dna", "da1", "da2", "sna", "sa1", "sa2", "sid"]

    def __init__(self, **kwargs) -> None:
        for attr in self.__attrs__:
            if attr not in kwargs:
                raise ValueError(f"Missing header name: {attr}")
            value = kwargs[attr]
            if not isinstance(value, bytes):
                raise ValueError(f"Header {attr} value must be in bytes")
            setattr(self, attr, kwargs[attr])

    def __iter__(self) -> Iterator:
        return iter(self.__dict__)

    @property
    def raw(self) -> bytes:
        """
        Returns the raw content of header, in bytes.
        """
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

    def __repr__(self) -> str:
        return "<FINS Header: {}>".format(self.raw)

    def __str__(self) -> str:
        return str(self.__dict__)

    @classmethod
    def from_bytes(cls, data: bytes) -> "Header":
        """
        Build a new Header instance from sequence of bytes.
        """
        if len(data) < 10:
            raise ValueError("Insufficient header data length")
        return cls(
            icf=data[0:1],
            rsv=data[1:2],
            gct=data[2:3],
            dna=data[3:4],
            da1=data[4:5],
            da2=data[5:6],
            sna=data[6:7],
            sa1=data[7:8],
            sa2=data[8:9],
            sid=data[9:10],
        )

    @classmethod
    def default(cls) -> "Header":
        """Returns default header."""
        return cls(
            icf=b"\x80",
            rsv=b"\x00",
            gct=b"\x02",
            dna=b"\x00",
            da1=b"\x00",
            da2=b"\x00",
            sna=b"\x00",
            sa1=b"\x01",
            sa2=b"\x00",
            sid=b"\x00",
        )
