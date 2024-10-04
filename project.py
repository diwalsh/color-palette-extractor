import os
import argparse
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial import distance


def main():
    """
    Main function to extract a color palette from an image.

    Parses command-line arguments, loads the image, extracts dominant colors,
    generates a palette image, and exports the color codes.
    """
    
    # Parse command-line arguments
    args = parse_arguments()

    # Load user image
    image = load_image(args.image)
    if image is None:
        return
    
    # Extract the filename without the extension
    base_filename = os.path.splitext(os.path.basename(args.image))[0]
    
    # Create 'palettes' directory if it doesn't exist
    output_dir = 'palettes'
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract dominant colors
    colors = extract_dominant_colors(image, args.colors, args.threshold)
    
    # Generate the palette image with codes
    palette_image = generate_palette_image(colors, args.format)
    palette_image.show()                                # preview image
    
    # Save image to Palettes Folder
    palette_image_path = os.path.join(output_dir, f'{base_filename}_palette.png')
    palette_image.save(palette_image_path)   # save image
    print(f"Color swatches saved to palettes/{base_filename}_palette.png")
    
    # Export the color codes in both formats (hex and rgb)
    export_color_codes(colors, base_filename, output_dir)
    
    
def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Namespace: Contains parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Extract a color palette from an image")
    
    parser.add_argument(
        '-i', '--image', 
        type=str, 
        required=True, 
        help="Path to the input image"
    )
    parser.add_argument(
        '-c', '--colors', 
        type=int, 
        default=5, 
        help="Number of dominant colors to extract (default is 5)"
    )
    parser.add_argument(
        '-f', '--format', 
        type=str, 
        choices=['hex', 'rgb'], 
        default='hex', 
        help="Format of the output color codes: 'hex' or 'rgb' (default is 'hex')"
    )
    parser.add_argument(
        '-t', '--threshold', 
        type=int, 
        default=40, 
        help="Threshold for color uniqueness (default is 40); the smaller the threshold, the more similar colors can be."
    )
    
    return parser.parse_args()


def load_image(filepath):
    """
    Load an image from a given file path.

    Args:
        filepath (str): The path to the image file.

    Returns:
        Image: The loaded image or None if loading fails.
    """
    try:
        image = Image.open(filepath)
        image.verify()                  # Check if it's an actual image file
        return Image.open(filepath)     # Re-open it for actual processing (after verification)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None
    except UnidentifiedImageError:
        print(f"Error: The file {filepath} is not a valid image.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
    
def extract_dominant_colors(image, num_colors, threshold, buffer=12):
    """
    Extract dominant colors from the image.

    Args:
        image (Image): The input image.
        num_colors (int): The number of colors to extract.
        threshold (int): The uniqueness threshold for color extraction.
        buffer (int): Extra buffer for k-means clustering (default is 12).

    Returns:
        list: A list of dominant colors in RGB format.
    """
    image = image.resize((300, 300))    # Resize for quicker processing
    data = np.array(image)              # Convert to NumPy Array
    pixels = data.reshape((-1, 3))      # Reshape to a list of pixels (-1 for length of array, 3 for RGB)
    
    # Instantiate a k-means model, using number of colors to extract, random state at 42
    kmeans = KMeans(n_clusters=num_colors + buffer, random_state=42)  
    kmeans.fit(pixels)                  # Train the model on modified image as pixel array
    
    colors = kmeans.cluster_centers_.astype(int)        # Dominant colors extracted as integer RGB values
    unique_colors = prioritize_unique_colors(colors, threshold)    # Prioritize unique colors
    return unique_colors[:num_colors]


def generate_palette_image(colors, format='hex'):
    """
    Generate an image palette from the provided colors.

    Args:
        colors (list): List of colors in RGB format.
        format (str): Format for the color codes ('hex' or 'rgb').

    Returns:
        Image: The generated palette image.
    """
    # Create a blank palette image: height = 150 (100 for swatch, 50 for text)
    palette_width = 100 * len(colors)  # 100 pixels wide per color
    palette = Image.new("RGB", (palette_width, 150), "white")
    draw = ImageDraw.Draw(palette)

    try:
        font = ImageFont.truetype("helvetica.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    for i, color in enumerate(colors):
        block = Image.new("RGB", (100, 100), tuple(color))  # Create a block of color (100x100 square)
        palette.paste(block, (i * 100, 0))

        # Title each swatch with the color code in the chosen format
        if format == 'hex':
            color_code = '#%02x%02x%02x' % tuple(color)
            text_position = (i * 100 + 32, 120)  # start cell + 32px padding, 120px from the top
        else:
            color_code = 'rgb(%d, %d, %d)' % tuple(color)
            text_position = (i * 100 + 10, 120)  # start cell + 10px padding, 120px from the top
        draw.text(text_position, color_code, fill="black", font=font)

    return palette


def export_color_codes(colors, filename, output_dir):
    """
    Export the extracted color codes to a text file.

    Args:
        colors (list): List of colors in RGB format.
        filename (str): Base filename for output files.
    """
    palette_file_path = os.path.join(output_dir, f'{filename}_palette.txt')
    with open(palette_file_path, 'w') as file:
        for color in colors: # Generate both hex and RGB formats
            hex_code = '#%02x%02x%02x' % tuple(color)
            rgb_code = 'rgb(%d, %d, %d)' % tuple(color)
            file.write(f"{hex_code} | {rgb_code}\n")
    
    print(f"Color codes saved to palettes/{filename}_palette.txt")
    
    
def prioritize_unique_colors(colors, threshold=40):
    """
    Prioritize unique colors based on the specified threshold.

    Args:
        colors (list): List of colors in RGB format.
        threshold (int): Threshold for uniqueness; smaller values allow more similar colors.

    Returns:
        list: A list of unique colors based on the threshold.
    """
    unique_colors = []
    for color in colors:    # return colors whose distances in 3D space from each other are greater than threshold
        if not any(distance.euclidean(color, existing_color) < threshold for existing_color in unique_colors):
            unique_colors.append(color)
    return unique_colors
    
    
if __name__ == "__main__":
    main()