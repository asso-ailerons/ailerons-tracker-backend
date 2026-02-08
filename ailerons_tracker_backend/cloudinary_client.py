"""Cloudinary Client"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename
from errors import CloudinaryError


cloudinary_config = cloudinary.config(secure=True)


def upload(image_name: str, image_path: str) -> str:
    """Upload an image and return a Cloudinary URL."""

    try:
        image_id = secure_filename(image_name)

        cloudinary.uploader.upload(
            image_path, public_id=image_id, unique_filename=False, overwrite=True
        )
    except Exception as e:
        raise CloudinaryError(e) from e

    url = cloudinary.CloudinaryImage(image_id).build_url()
    return url
