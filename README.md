# fins-driver

FINS (Factory Interface Network Service) Python driver for Omron PLC.

## Installation

Install the latest version from PyPI by typing this command:

    pip install -U fins-driver

## Usage

Below is an example on how to use the client class.

```python
from fins import FinsClient

client = FinsClient(host='192.168.250.1', port=9600)
response = client.memory_area_read('D0')
print(response.data)
client.close()
```

## Memory Area Read

`.memory_area_read(address: str | bytes, num_items: int = 1) -> Response`

Examples:

Read DM area at word 0.

```python
response = client.memory_area_read('D0')
```

Read CIO area at word 100 and bit 01.

```python
response = client.memory_area_read('CIO100.01')
```

## Memory Area Write

`.memory_area_write(address: str | bytes, data: bytes, num_items: int = 1) -> Response`

Examples:

Write to CIO area at word 100. It will turn on CIO100.00 and CIO100.01. Hex
value \x00\x03 is translated to 0000 0000 0000 0011 in binary.

```python
response = client.memory_area_write("CIO100", b"\x00\x03")
```

Write to CIO area at word 100 and bit 01. We only need to provide 1 bytes data
to write bit status. Hex value \x01 is translated to ON, while \x00 is
translated to OFF.

```python
response = client.memory_area_write("CIO100.01", b"\x01")
```

## Memory Area Fill

`.memory_area_fill(address: str | bytes, data: bytes, num_items: int = 1) -> Response`

Examples:

Fill DM area word with \x00\x03.

```python
response = client.memory_area_fill("D0", b"\x00\x03")
```

## Multiple Memory Area Read

`.multiple_memory_area_read(*addresses: str | bytes) -> Response`

Examples:

Read multiple memory area words.

```python
response = client.multiple_memory_area_read("D0", "D1")
```

Read multiple memory area bits.

```python
response = client.multiple_memory_area_read("CIO100.00", "CIO100.01")
```

## Memory Area Transfer

`.memory_area_transfer(source_address: str | bytes, dest_address: str | bytes, num_items: int = 1) -> Response`

Examples:

Transfer memory area word from D0 to D1.

```python
response = client.memory_area_transfer("D0", "D1")
```

## Run

`.run(mode: debug | monitor | run = "monitor", program_number: bytes = b"\xff\xff") -> Response`

Examples:

Change PLC to run in monitor mode.

```python
response = client.run("monitor")
```

## Stop

`.stop()`

Examples:

Stop PLC device.

```python
response = client.stop()
```

## Forced Set/Reset

`.forced_set_reset(*specs: SetResetSpec) -> Response`

Examples:

Force-set ON the CIO.01.

```python
from fins import SetResetSpecCode, SetResetSpec

response = client.forced_set_reset(SetResetSpec(SetResetSpecCode.FORCE_SET, "CIO0.01"))
```

## Forced Set/Reset Cancel

`.forced_set_reset_cancel()`

Examples:

Cancel all bits that have been forced ON or OFF.

```python
response = client.forced_set_reset_cancel()
```

You can also find more examples in the [samples](samples/) folder.

## Memory Areas

Below is supported memory areas prefix.

| Prefix |   Description    |
| ------ | ---------------- |
| CIO    | Core IO area     |
| W      | Work area        |
| H      | Holding area     |
| A      | Auxiliary area   |
| D      | Data Memory area |

## Response Object

| Property/Method |   Type    |                   Description                   |
| --------------- | --------- | ----------------------------------------------- |
| data            | `bytes`   | Response data                                   |
| code            | `bytes`   | Response code, primarily \x00\x00 if it's OK    |
| status_text     | `str`     | Textual description of the response code        |
| ok              | `bool`    | True if request was OK (Normal completion)      |
| raw             | `bytes`   | The overall raw content of response             |
| header          | `Header`  | Response header data                            |
| command         | `Command` | The request command that was sent to the device |

## License

MIT
