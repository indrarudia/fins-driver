import time

from fins import FinsClient


def main() -> None:
    client = FinsClient(host="192.168.250.1")
    client.connect()

    try:
        while True:
            response = client.memory_area_read("D100")
            print("counter:", int.from_bytes(response.data, "big"))
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()


if __name__ == "__main__":
    main()
