import base64


def encode(string_to_encode: str):
    str_bytes = string_to_encode.encode("ascii")
    base64_bytes = base64.b64encode(str_bytes)
    base64_string = base64_bytes.decode("ascii")

    return base64_string
