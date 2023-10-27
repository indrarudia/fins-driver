# fins-driver

FINS (Factory Interface Network Service) Python Driver for Omron PLC.

## Installation

Install the latest version from PyPI by typing this command:

    pip install -U fins-driver

## Usage

- Memory Area Read

```python
from fins import FinsClient

client = FinsClient(host='192.168.250.1', port=9600)

# Read Data Memory area at word 0.
response = client.memory_area_read('D0')

# Read CIO area at word 100 and its bit status at 1.
response = client.memory_area_read('CIO100.01')

print('Data:', response.data)
print('Code:', response.code)
print('Status text:', response.status_text)
print('Raw data:', response.raw)

client.close()
```

- Memory Area Write

```python
from fins import FinsClient

client = FinsClient(host="192.168.250.1", port=9600)

# Write to CIO area at word 100. It will turn on CIO100.00 and CIO100.01. Hex
# value 0x0003 is translated to 0000 0000 0000 0011 in binary.
response = client.memory_area_write("CIO100", b"\x00\x03")

# Write to CIO area at word 100 and bit 01. We only need to provide 1 bytes data
# to write bit status. Hex value 0x01 is translated to ON, while 0x00 is
# translated to OFF.
response = client.memory_area_write("CIO100.01", b"\x01")

client.close()
```

You can also find more in the [samples](samples/) folder.

## Memory Areas

Below is supported memory areas prefix.

| Prefix |    Description    |
| ------ | ----------------- |
| CIO    | Core IO area.     |
| W      | Work area.        |
| H      | Holding area.     |
| A      | Auxiliary area.   |
| D      | Data Memory area. |

## Response Object

| Property/Method |   Type    |                   Description                    |
| --------------- | --------- | ------------------------------------------------ |
| data            | `bytes`   | Response data.                                   |
| code            | `bytes`   | Response code, primarily `0x0000` if it's OK.    |
| status_text     | `str`     | Textual description of the response code.        |
| ok              | `bool`    | True if request was OK (Normal completion).      |
| raw             | `bytes`   | The overall raw content of response.             |
| header          | `Header`  | Response header data.                            |
| command         | `Command` | The request command that was sent to the device. |

## License

MIT
