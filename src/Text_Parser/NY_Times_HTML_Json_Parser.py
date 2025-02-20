import os
import json
from bs4 import BeautifulSoup

output_file_path = 'extracted_content.json'
all_content = []

# Loop through all files in the current directory
for filename in os.listdir('.'):
    # Check if the file is an HTML file
    if filename.endswith('.html'):
        # Read the HTML file
        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'lxml')

        # Extract title using your existing logic
        title_tag = soup.find('title')
        title_text = title_tag.text if title_tag else 'Title not found'

        # Extract content from <p> tags with class "css-at9mc1 evys1bk0"
        paragraphs = soup.find_all('p', class_="css-at9mc1 evys1bk0")
        content_text = '\n'.join([paragraph.text for paragraph in paragraphs])

        # Remove all non-ASCII characters
        title_text = title_text.encode('ascii', 'ignore').decode('ascii')
        content_text = content_text.encode('ascii', 'ignore').decode('ascii')

        # Change the fifth character from '-' to ':' in the file title
        if len(filename) > 5 and filename[4] == '-':
            formatted_filename = filename[:4] + ':' + filename[5:]
        else:
            formatted_filename = filename

        # Remove the '.html' extension for the topic
        topic = formatted_filename.replace('.html', '')

        # Create a dictionary for the current file's content
        file_content = {
            "Topic": topic,
            "Title": title_text,
            "Content": content_text
        }

        # Append the dictionary to the list
        all_content.append(file_content)

# Write the list of dictionaries to a JSON file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(all_content, output_file, indent=4)

