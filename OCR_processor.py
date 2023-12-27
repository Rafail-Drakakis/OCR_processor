import os
import PIL.Image
import pytesseract

'''
training data found in the git repo of the pytesseract
https://github.com/tesseract-ocr/tessdata/tree/main
'''

def get_filenames_by_extension(extensions):
    """
    The function `get_filenames_by_extension` returns a sorted list of filenames in the current
    directory that have a specified extension.
    
    :param extensions: extensions is a list of file extensions
    :return: The function `get_filenames_by_extension` returns a sorted list of filenames in the current
    directory that have the specified extensions.
    """
    current_directory = os.getcwd()
    filenames = [filename for filename in os.listdir(current_directory) if filename.endswith(tuple(extensions))]
    return sorted(filenames)

def extract_images_to_text(image_paths, output_file_path, languages, tessdata_path):
    """
    The function `extract_images_to_text` takes a list of image paths, an output file path, a language
    or list of languages, and a path to the tessdata directory, and extracts text from the images using
    Tesseract OCR, saving the extracted text to the output file.
    
    :param image_paths: A list of file paths to the images you want to extract text from
    :param output_file_path: The output file path is the path where the extracted text will be saved. It
    should be a string representing the file path, including the file name and extension.
    :param languages: The "languages" parameter is a string or a list of strings specifying the
    languages to be used for text extraction. It can be a single language code (e.g., "eng" for English)
    or a list of multiple language codes (e.g., ["eng", "spa"] for English and
    :param tessdata_path: The `tessdata_path` parameter is the path to the directory where the Tesseract
    OCR data files are located. These data files contain language-specific information and are necessary
    for Tesseract to accurately recognize text in different languages
    :return: the path of the output file where the extracted text from the images is written.
    """
    os.environ['TESSDATA_PREFIX'] = tessdata_path
    texts = []

    for image_path in image_paths:
        try:
            with PIL.Image.open(image_path).convert('L') as img:
                text = pytesseract.image_to_string(img, lang=languages)
                if text:
                    texts.append(f"Languages: {languages} - File: {os.path.basename(image_path)}\n{text}\n")
        except (OSError, pytesseract.TesseractError) as e:
            texts.append(f"Error processing image {os.path.basename(image_path)}: {e}\n")

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.writelines(texts)

    return output_file_path

if __name__ == "__main__":
    tessdata_path = "test_data/"  # Modify the path if you have the test files in a different directory
    extensions = input("Enter the filenames separated by space (e.g., test.png, test.jpg): ").split()
    output_file = input("Enter the output filename (e.g., output.txt): ")
    while not output_file.endswith('.txt'):
        print("Invalid output filename. Please choose a .txt output filename.")
        output_file = input("Enter the output file path: ")
    
    languages = input("Enter languages separated by '+' (e.g., eng+fra+rus): ")
    
    image_paths = get_filenames_by_extension(extensions)
    extract_images_to_text(image_paths, output_file, languages, tessdata_path)