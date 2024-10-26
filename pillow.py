from PIL import Image
import os
from django.conf import settings
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

def process_image(image, max_width=1024, max_height=768, quality=85):
    # Open the uploaded image
    img = Image.open(image)

    # Get the original size
    original_width, original_height = img.size

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Set target dimensions while preserving the aspect ratio
    if aspect_ratio > 1:  # Landscape
        target_width = min(max_width, original_width)
        target_height = int(target_width / aspect_ratio)
    else:  # Portrait or square
        target_height = min(max_height, original_height)
        target_width = int(target_height * aspect_ratio)

    # Resize the image to the target size
    img = img.resize((target_width, target_height), Image.LANCZOS)

    # Create a new filename with .jpeg extension
    base_filename, _ = os.path.splitext(image.name)
    new_filename = f"{base_filename}.jpg"

    # Save the processed image to a BytesIO object
    output = BytesIO()
    img.convert('RGB').save(output, format='JPEG', quality=quality)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        None,
        new_filename,
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )


def processimage(image, max_width=1024, max_height=768, quality=85):
    # Open the uploaded image
    img = Image.open(image)

    # Get the original size
    original_width, original_height = img.size

    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height

    # Set target dimensions while preserving the aspect ratio
    if aspect_ratio > 1:  # Landscape
        target_width = min(max_width, original_width)
        target_height = int(target_width / aspect_ratio)
    else:  # Portrait or square
        target_height = min(max_height, original_height)
        target_width = int(target_height * aspect_ratio)

    # Resize the image to the target size
    img = img.resize((target_width, target_height), Image.LANCZOS)

    # Create a new filename with .jpeg extension
    base_filename, _ = os.path.splitext(image.name)
    new_filename = f"{base_filename}.jpg"

    # Save the processed image to a BytesIO object
    output = BytesIO()
    img.convert('RGB').save(output, format='JPEG', quality=quality)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        None,
        new_filename,
        'image/jpeg',
        output.getbuffer().nbytes,
        None
    )
