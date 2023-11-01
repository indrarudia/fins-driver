import binascii
import datetime
import time

from fins import FinsClient


def main() -> None:
    client = FinsClient(host="192.168.250.1")
    client.connect()

    try:
        while True:
            response = client.memory_area_read("D0")
            print(
                datetime.datetime.now(),
                "response:",
                binascii.hexlify(response.raw, b" ", 2),
                "value:",
                int.from_bytes(response.data, "big"),
                "status:",
                response.code,
            )
            time.sleep(1 / 100)
    except KeyboardInterrupt:
        client.close()


if __name__ == "__main__":
    main()
