import os
import glob
import random
from PIL import Image, ImageFile

# Set PIL to allow truncated images (optional)
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Define dataset path for images
DATASET_PATH = "./images-sample"
MAX_VALID_IMAGES = 500  # The target number of valid images

def cleanup_images():
    # Get list of all .jpg images in the dataset folder
    image_files = glob.glob(os.path.join(DATASET_PATH, "*.jpg"))
    
    valid_images = []
    corrupted_images = []

    # Check each image
    for image_file in image_files:
        try:
            # Try opening the image and verifying its integrity
            img = Image.open(image_file)
            img.verify()  # This will raise an exception if the image is corrupted
            valid_images.append(image_file)
        except (OSError, Image.DecompressionBombError) as e:
            # If error occurs, the image is corrupted
            corrupted_images.append(image_file)
            continue
    
    # Output the results
    print(f"Total images found: {len(image_files)}")
    print(f"Corrupted images found: {len(corrupted_images)}")
    print(f"Valid images found: {len(valid_images)}")

    # Remove corrupted images
    for corrupted_image in corrupted_images:
        print(f"Removing corrupted image: {corrupted_image}")
        os.remove(corrupted_image)
    
    # If valid images exceed the target (500), remove extra ones
    if len(valid_images) > MAX_VALID_IMAGES:
        images_to_delete = len(valid_images) - MAX_VALID_IMAGES
        print(f"Deleting {images_to_delete} extra valid images to reduce to {MAX_VALID_IMAGES}")
        
        # Randomly shuffle and delete images
        random.shuffle(valid_images)
        images_to_remove = valid_images[:images_to_delete]
        
        for image_to_remove in images_to_remove:
            print(f"Removing extra image: {image_to_remove}")
            os.remove(image_to_remove)
    
    print(f"Cleanup complete. Remaining valid images: {MAX_VALID_IMAGES}")

if __name__ == "__main__":
    cleanup_images()
