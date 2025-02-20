from PIL import Image
from pdf2image import convert_from_path
import pytesseract

# Load an image
image = Image.open('article62.png')

# Use tesseract to do OCR on the image
text = pytesseract.image_to_string(image)

# Split the text into lines
lines = text.split('\n')

# Reconstruct the paragraphs and remove hyphenation
new_text = []
paragraph = []
for line in lines:
    # Check if the line ends with a hyphen and merge with next line
    if line.endswith('-'):
        line = line.rstrip('-')
        if paragraph:
            paragraph[-1] = paragraph[-1] + line
        else:
            paragraph.append(line)
    elif line.strip():
        paragraph.append(line.strip())
    elif paragraph:
        # If there's a blank line and we have collected some text, start a new paragraph
        new_text.append(' '.join(paragraph))
        paragraph = []

# Add the last paragraph if it exists
if paragraph:
    new_text.append(' '.join(paragraph))

# Join the paragraphs with double newlines to separate them
formatted_text = '\n\n'.join(new_text)

with open('output.txt', 'w') as file:
    file.write(formatted_text)
