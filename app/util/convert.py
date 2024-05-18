import base64


def encode_image_from_path(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def encode_image_base64(image: bytes) -> str:
    return base64.b64encode(image).decode("utf-8")
