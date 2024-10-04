import os
import pytest
from PIL import Image
import numpy as np
from project import (
    load_image,
    extract_dominant_colors,
    generate_palette_image,
    export_color_codes,
    prioritize_unique_colors,
)


# Create a dummy image for testing
@pytest.fixture
def dummy_image(tmp_path):
    # Create a simple gradient image (100x100) with multiple colors
    image_path = tmp_path / "test_image.png"
    image = Image.new("RGB", (100, 100))

    # Create a gradient
    for x in range(100):
        for y in range(100):
            r = int(x * 255 / 100)  # Red gradient
            g = int(y * 255 / 100)  # Green gradient
            b = 128  # Constant blue
            image.putpixel((x, y), (r, g, b))
    
    image.save(image_path)
    return image_path

def test_load_image(dummy_image):
    image = load_image(dummy_image)
    assert image is not None
    assert image.size == (100, 100)

def test_extract_dominant_colors(dummy_image):
    image = load_image(dummy_image)
    colors = extract_dominant_colors(image, num_colors=5, threshold=30)
    assert len(colors) == 5  # Should extract 5 colors
    for color in colors:
        assert isinstance(color, np.ndarray)  # Check if colors are in array format

def test_generate_palette_image(dummy_image):
    image = load_image(dummy_image)
    colors = extract_dominant_colors(image, num_colors=5, threshold=30)
    palette_image = generate_palette_image(colors, format='hex')
    assert palette_image.size[1] == 150  # Palette image height should be 150
    assert len(colors) == palette_image.size[0] // 100  # Check number of color blocks

def test_export_color_codes(dummy_image, tmp_path):
    image = load_image(dummy_image)
    colors = extract_dominant_colors(image, num_colors=5, threshold=30)
    output_dir = tmp_path / "palettes"
    output_dir.mkdir()
    export_color_codes(colors, "test_output", str(output_dir))
    assert os.path.exists(os.path.join(output_dir, "test_output_palette.txt"))

def test_prioritize_unique_colors():
    colors = np.array([[255, 0, 0], [255, 10, 10], [0, 255, 0]])
    unique_colors = prioritize_unique_colors(colors, threshold=15)
    assert len(unique_colors) == 2  # Two colors should be unique based on the threshold


if __name__ == "__main__":
    pytest.main()
