# Color-Palette Extractor
#### Video Demo: https://youtu.be/Mj71CkwLdmE

#### Description:
The **Image Color-Palette Extractor** is a Python-based command-line application designed to analyze images and extract their dominant colors. It presents these colors in a visually simplified palette format, paired with chosen color-code-format (hex or rgb). This project utilizes various Python libraries, including Pillow for image processing and sci-kit learn for color clustering, to create an easy way to generate color palettes from images. There is a threshold variable, which allows users to decide how unique each color must be within the palette.

### Functionality
The main functionality of the application includes:

1. **Image Loading**: The application supports various image formats, allowing users to input images directly from their file system.
   
2. **Color Extraction**: Utilizing k-means clustering, the application extracts the dominant colors from the input image. Users can specify the number of colors to be extracted and a threshold for color differentiation, which helps in customizing the palette to their preferences.

3. **Palette Generation**: Once the dominant colors are extracted, the application generates a visual representation of the color palette. Each color swatch is displayed along with its corresponding hex or RGB values for easy reference.

4. **File Output**: The application saves the generated color palette as an image file and exports both the hex and rgb color codes into a text file. Both files are named according to the original image, making it easy to manage multiple palettes.

### File Structure
The project is organized into these files:

- `project.py`: The main script that orchestrates the loading of images, extraction of colors, generation of the palette image, and saving output files.
- `test_project.py`: Contains unit tests in PyTest that validate the functionality of the color extraction and palette generation processes. 
- `requirements.txt`: All libraries needed to run the program.

### Design Choices

- **User Customization**: Allowing users to specify the number of colors and a threshold for differentiation gives them control over the output, catering to various needs and artistic preferences. Users can also choose between hex and rgb codes for inclusion on their palette images.

- **Use of Libraries**: Leveraging libraries such as Pillow and sci-kit learn not only simplifies the coding process but also ensures the application can handle a wide range of image types and perform efficient clustering for color extraction.

- **Output Formats**: Providing both visual and text outputs caters to different preferences, whether they are looking for a quick visual reference or need to use the color codes in design applications.

### Future Enhancements
While the current version of the application is functional and meets the primary goals, there are several potential enhancements for future iterations:

- **Interactive GUI**

- **Advanced Color Algorithms**

- **Integration with Design Tools**

This project aims to provide a simple yet effective way to extract and visualize colors from images, catering to artists, designers, and anyone interested in color theory.
