from PIL import Image
import numpy as np
import io

def extract_value(
    text,
    key
):

    try:

        start = text.find(
            key + ":"
        )

        if start == -1:

            return ""

        start += (
            len(key) + 1
        )

        remaining = text[start:]

        value = (
            remaining
            .split("\n")[0]
            .strip()
        )

        return value

    except:

        return ""


def image_to_bytes(image):

    buffer = io.BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    return buffer.getvalue()

ef extract_red_region(image_bytes):

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    img = np.array(image)

    red_mask = (
        (img[:,:,0] > 180)
        &
        (img[:,:,1] < 100)
        &
        (img[:,:,2] < 100)
    )

    coords = np.argwhere(red_mask)

    if len(coords) == 0:
        return image

    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)

    padding = 30

    x_min = max(0, x_min-padding)
    y_min = max(0, y_min-padding)

    x_max = min(
        image.width,
        x_max+padding
    )

    y_max = min(
        image.height,
        y_max+padding
    )

    cropped = image.crop(
        (
            x_min,
            y_min,
            x_max,
            y_max
        )
    )

    return cropped
