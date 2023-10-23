import binascii
import time

from fins import Client, Command
from fins.command import MEMORY_AREA_READ
from fins.memory_area import DATA_MEMORY_WORD


def main() -> None:
    command = Command(
        code=MEMORY_AREA_READ,
        text=DATA_MEMORY_WORD + b"\x00\x00\x00" + b"\x00\x01",
    )

    client = Client(host="192.168.250.1")
    client.connect()

    try:
        while True:
            r = client.send(command)
            data = r.data
            print(
                "response:",
                binascii.hexlify(data, b" ", 2),
                "value:",
                int.from_bytes(data[-2:]),
            )
            time.sleep(0.05)
    except KeyboardInterrupt:
        client.close()


if __name__ == "__main__":
    main()
