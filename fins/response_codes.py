RESPONSE_CODES = {
    b"\x00\x00": "Normal completion",
    b"\x00\x01": "Service was interrupted",
    b"\x01\x01": "Local not not part of Network",
    b"\x01\x02": "Token time-out, node number too large",
    b"\x01\x03": "Number of transmit retries exceeded",
    b"\x01\x04": "Maximum number of frames exceeded",
    b"\x01\x05": "Node number setting error (range)",
    b"\x01\x06": "Node number duplication error",
}
