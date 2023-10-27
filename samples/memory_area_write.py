from fins import FinsClient


def main() -> None:
    client = FinsClient(host="192.168.250.1")
    client.connect()
    response = client.memory_area_write("CIO100.1", b"\x01")

    print("Data:", response.data)
    print("Code:", response.code)
    print("Status text:", response.status_text)

    client.close()


if __name__ == "__main__":
    main()
