from PIL import Image
import random
import os

def check_image_properties(image_path):
    # Open the image using Pillow
    with Image.open(image_path) as img:
        # Get image size
        width, height = img.size
        print(f"Image Size: {width} x {height} pixels")

        # Get image format
        print(f"Image Format: {img.format}")

        # Get image mode (e.g., 'RGB', 'L' for grayscale, etc.)
        print(f"Image Mode: {img.mode}")

        # Display additional details
        if img.format in ['JPEG', 'PNG']:
            print(f"Image Quality: Usually 85 for JPEG, 100 for PNG (lossless)")

# Example usage
check_image_properties('static/assets/img/land/rangeroverlodge.jpg')

# Paths
MEDIA_DIR = 'media/cars'
STATIC_CARS_DIR = 'static/assets/img/cars'

# Ensure the target directory exists
if not os.path.exists(STATIC_CARS_DIR):
    os.makedirs(STATIC_CARS_DIR)

# Get all image files from the media directory
image_extensions = ('.jpg', '.jpeg', '.png', '.gif')  # Define allowed image formats
media_files = [f for f in os.listdir(MEDIA_DIR) if f.lower().endswith(image_extensions)]

# Randomly select 20 images from the media folder
random_images = random.sample(media_files, min(20, len(media_files)))

# Loop through each randomly selected image
for image_file in random_images:
    try:
        # Open the image using Pillow
        image_path = os.path.join(MEDIA_DIR, image_file)
        img = Image.open(image_path)

        # Keep the original file name and save it to the static cars folder
        save_path = os.path.join(STATIC_CARS_DIR, image_file)

        # Save the image in the static cars directory
        img.save(save_path)

        print(f'Successfully saved {image_file} to {STATIC_CARS_DIR}')
    except Exception as e:
        print(f"Failed to process {image_file}: {str(e)}")