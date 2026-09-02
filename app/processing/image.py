from PIL import Image, UnidentifiedImageError
from io import BytesIO
from app.processing.image_analysis import analyze_image
def process_image(image_data: bytes):
    try:
        image= Image.open (BytesIO(image_data))
        analysis= analyze_image(image)
        return{"valid": True,
            "width": image.width,
            "height": image.height,
            "format": image.format,
            "analysis": analysis}
    except UnidentifiedImageError:
        return{"valid": False,
               "error": "invalid or unsupported image file"
        }