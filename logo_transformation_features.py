import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, UnidentifiedImageError
from bs4 import BeautifulSoup
import cairosvg
import random
import numpy as np


# Define a custom CairoSVGError class to handle CairoSVG specific errors
class CairoSVGError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Function to add watermark to an image
def add_watermark_at_bottom_right(input_image_path, output_image_path, watermark_text):
    try:
        img = Image.open(input_image_path).convert("RGBA")
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {input_image_path}")
        return
    print('Adding Watermark at bottom right corner')

    # Enhance brightness of alpha channel
    alpha = img.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.8)
    img.putalpha(alpha)

    # Add text watermark at bottom right corner
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    textwidth, textheight = draw.textsize(watermark_text, font)
    width, height = img.size
    x = width - textwidth - 10
    y = height - textheight - 10

    # Apply the watermark text
    draw.text((x, y), watermark_text, font=font, fill=(220, 220, 220, 128))

    img = img.convert("RGB")
    img.save(output_image_path, "PNG")


# Function to add watermark to an image
def add_watermark_diagonally(input_image_path, output_image_path, watermark_text):
    try:
        img = Image.open(input_image_path).convert("RGBA")
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {input_image_path}")
        return
    print("Adding Watermark diagonally")

    # Adding diagonal text watermark
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Calculate text size
    textwidth, textheight = draw.textsize(watermark_text, font)

    # Create a new image for the text
    text_img = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw_text = ImageDraw.Draw(text_img)

    # Calculate the position for the text
    width, height = img.size
    x = -width // 4  # Starting position (can be adjusted)
    y = height - textheight  # Start from the bottom

    # Draw text repeatedly across the image diagonally
    while y > -height:
        draw_text.text((x, y), watermark_text, font=font, fill=(220, 220, 220, 128))
        x += textwidth
        y -= textheight

    # Rotate the text image to cover from bottom left to top right
    text_img = text_img.rotate(35, expand=1)

    # Ensure the rotated image is the same size as the original
    text_img = text_img.resize(img.size, Image.ANTIALIAS)

    # Combine images
    img = Image.alpha_composite(img, text_img)

    img = img.convert("RGB")
    img.save(output_image_path, "PNG")


# Function to add rotation, brightness, and Gaussian blur
def add_rotation_brightness_gaussian_blur(input_image_path, output_image_path, watermark_text=None):
    try:
        img = Image.open(input_image_path).convert("RGBA")
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {input_image_path}")
        return
    print("Adding Rotation, Brightness and Gaussian Blur")

    # Apply random rotation
    angle = random.randint(-15, 15)
    img = img.rotate(angle, expand=True)

    # Apply random brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.25, 0.5))

    # Apply Gaussian blur
    img = img.filter(ImageFilter.GaussianBlur(radius=random.randint(0, 4)))

    img = img.convert("RGB")
    img.save(output_image_path, "PNG")


# Function to add rotation and grey-colored mesh
def add_rotation_grey_colored_mesh(input_image_path, output_image_path, watermark_text=None):
    try:
        img = Image.open(input_image_path).convert("RGBA")
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {input_image_path}")
        return
    print("Adding Rotation, Grey colored mesh")
    width, height = img.size

    # Apply random rotation
    angle = random.randint(-15, 15)
    img = img.rotate(angle, expand=True)

    # Create a blank image with the same size and mode
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))

    # Create a drawing context
    draw = ImageDraw.Draw(overlay)

    # Set grid size and line color
    grid_size = 2  # Adjust as needed
    line_color = (128, 128, 128, 80)  # Grey color with transparency

    # Draw horizontal grid lines
    for y in range(0, height, grid_size):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)

    # Draw vertical grid lines
    for x in range(0, width, grid_size):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)

    # Composite the overlay onto the original image
    result = Image.alpha_composite(img, overlay)

    result = result.convert("RGB")
    result.save(output_image_path, "PNG")


# Function to add Gaussian noise
def add_gaussian_noise(img, mean=0, std=1):
    np_img = np.array(img)
    noise = np.random.normal(mean, std, np_img.shape)
    np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(np_img, 'RGBA')


# Function to add Gaussian noise
def add_gaussian_noise_to_logo(input_image_path, output_image_path, watermark_text=None):
    try:
        img = Image.open(input_image_path).convert("RGBA")
    except UnidentifiedImageError:
        print(f"Cannot identify image file: {input_image_path}")
        return
    print("Adding Gaussian Noise and JPEG Compression")

    # Add Gaussian Noise to the image
    img = add_gaussian_noise(img, mean=1, std=0.5)

    # Save the perturbed image
    img = img.convert("RGB")
    img.save(output_image_path, format='PNG')


# Function to handle SVG files
def handle_svg(input_svg_path, output_image_path, watermark_text):
    try:
        # Convert SVG to PNG
        png_temp_path = input_svg_path.replace(".svg", ".png")
        cairosvg.svg2png(url=input_svg_path, write_to=png_temp_path)

        function_to_call = random.choice([add_watermark_at_bottom_right, add_watermark_diagonally, add_rotation_brightness_gaussian_blur, add_rotation_grey_colored_mesh, add_gaussian_noise_to_logo])

        # Add watermark to the converted PNG image
        function_to_call(png_temp_path, output_image_path, watermark_text)

        # Clean up the temporary PNG file
        os.remove(png_temp_path)
    except CairoSVGError as e:
        print(f"Error converting SVG: {e}")
    except UnidentifiedImageError as e:
        print(f"Cannot identify image file: {input_svg_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Main folder containing all subfolders
main_folder = "PATH_TO_DOWNLOADED_WEBPAGE_RESOURCES_FOLDER"

# Iterate through each subfolder (each containing 'rogerebert.com' and similar subfolders)
for folder_name in os.listdir(main_folder):
    folder_path = os.path.join(main_folder, folder_name)
    if not os.path.isdir(folder_path):
        continue

    # Paths within the current subfolder
    local_resources_path = os.path.join(folder_path, "local_resources")
    index_html_path = os.path.join(folder_path, "index.html")
    modified_html_path = os.path.join(folder_path, "feature_20_added.html")

    # Iterate through local_resources to find .png and .svg images
    for root, dirs, files in os.walk(local_resources_path):
        for file in files:
            if file.endswith('.png') or file.endswith('.svg'):
                file_path = os.path.join(root, file)
                # Skip processing if the file ends with "_modified.png"
                if file.endswith('_modified.png'):
                    continue
                output_path = os.path.join(root, f"{os.path.splitext(file)[0]}_modified.png")
                if file.endswith('.png'):
                    function_to_call = random.choice([add_watermark_at_bottom_right, add_watermark_diagonally, add_rotation_brightness_gaussian_blur, add_rotation_grey_colored_mesh, add_gaussian_noise_to_logo])

                    function_to_call(file_path, output_path, "Logo Copyright")
                elif file.endswith('.svg'):
                    handle_svg(file_path, output_path, "Logo Copyright")

    # Copy index.html to modified.html
    shutil.copy(index_html_path, modified_html_path)

    # Parse modified.html and update img tags
    with open(modified_html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    for img in soup.find_all('img'):
        found_logo = False
        for attr in img.attrs.values():
            if isinstance(attr, str) and ('logo' in attr or 'brand' in attr or 'branding' in attr):
                found_logo = True
                break

        if found_logo:
            src = img.get('src')
            if src and src.startswith('local_resources/'):
                filename = os.path.basename(src)
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}_modified.png"
                new_value = src.replace(filename, new_filename)
                img['src'] = new_value

    # Write changes to modified.html
    with open(modified_html_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

print("Processing complete.")
