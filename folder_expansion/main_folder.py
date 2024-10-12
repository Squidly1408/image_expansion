import os
from PIL import Image

def blend_pixels(pixel1, pixel2, factor):
    """Blends two pixels' color values by a given factor."""
    return tuple(int(p1 + (p2 - p1) * factor) for p1, p2 in zip(pixel1, pixel2))

def expand_image_with_blended_pixels(image, n):
    """Expands the image by adding n interpolated pixels between each original pixel."""
    width, height = image.size
    original_pixels = image.load()

    # Calculate new image dimensions
    new_width, new_height = width + (width - 1) * n, height + (height - 1) * n
    new_image = Image.new("RGB", (new_width, new_height))
    new_pixels = new_image.load()

    # Iterate through the original image and place the pixels in the new image
    for y in range(height):
        for x in range(width):
            # Place the original pixel
            new_pixels[x * (n + 1), y * (n + 1)] = original_pixels[x, y]

            # Horizontal blending
            if x < width - 1:
                for i in range(1, n + 1):
                    factor = i / (n + 1)
                    new_pixels[x * (n + 1) + i, y * (n + 1)] = blend_pixels(original_pixels[x, y], original_pixels[x + 1, y], factor)

            # Vertical blending
            if y < height - 1:
                for i in range(1, n + 1):
                    factor = i / (n + 1)
                    new_pixels[x * (n + 1), y * (n + 1) + i] = blend_pixels(original_pixels[x, y], original_pixels[x, y + 1], factor)

            # Diagonal blending (both horizontal and vertical)
            if x < width - 1 and y < height - 1:
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                        factor_x = i / (n + 1)
                        factor_y = j / (n + 1)
                        horizontal_blend = blend_pixels(original_pixels[x, y], original_pixels[x + 1, y], factor_x)
                        vertical_blend = blend_pixels(original_pixels[x, y + 1], original_pixels[x + 1, y + 1], factor_x)
                        new_pixels[x * (n + 1) + i, y * (n + 1) + j] = blend_pixels(horizontal_blend, vertical_blend, factor_y)

    return new_image

def process_folder(input_folder, output_folder, n):
    """Processes all images in the input folder and saves the expanded images to the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"expanded_{filename}")
            
            try:
                # Open the image and expand it
                image = Image.open(image_path)
                expanded_image = expand_image_with_blended_pixels(image, n)

                # Save the expanded image to the output folder
                expanded_image.save(output_path)
                print(f"Processed and saved: {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    # Folder paths
    input_folder = "folder_conversion/input_images"  # Folder containing the images to process
    output_folder = "folder_conversion/output_images"  # Folder where the processed images will be saved

    # Set the number of pixels to be added between each pair (n)
    n = 2  # Change this to control how many pixels to insert between

    # Process the entire folder
    process_folder(input_folder, output_folder, n)
