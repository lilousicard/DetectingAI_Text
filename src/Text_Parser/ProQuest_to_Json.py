import re
import json

def parse_document(file_path):
    articles = []

    # Read the entire document content
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define a pattern to split the document into articles.
    articles_content = content.split('**************************************************')

    # Define regular expressions for extracting different parts of each article
    title_pattern = re.compile(r'Title: (.*?)\n')
    publication_title_pattern = re.compile(r'Publication title: (.*?)\n')
    publication_date_pattern = re.compile(r'Publication date: (.*?)\n')
    issn_pattern = re.compile(r'ISSN: (.*?)\n')
    document_id_pattern = re.compile(r'ProQuest document ID: (.*?)\n')
    url_pattern = re.compile(r'Document URL: (.*?)\n')

    # The content pattern needs to capture everything after "Full text: " up to the next recognized section, which might start with any field
    content_pattern = re.compile(r'Full text: (.*?)(?=\n(?:Title:|Publication title:|Publication date:|ISSN:|ProQuest document ID:|Document URL:))', re.DOTALL)

    for article in articles_content:
        title_match = title_pattern.search(article)
        publication_title_match = publication_title_pattern.search(article)
        publication_date_match = publication_date_pattern.search(article)
        issn_match = issn_pattern.search(article)
        document_id_match = document_id_pattern.search(article)
        url_match = url_pattern.search(article)
        content_match = content_pattern.search(article)

        # Extract content and metadata, if present
        title = title_match.group(1) if title_match else ""
        publication_title = publication_title_match.group(1) if publication_title_match else ""
        publication_date = publication_date_match.group(1) if publication_date_match else ""
        issn = issn_match.group(1) if issn_match else ""
        document_id = document_id_match.group(1) if document_id_match else ""
        url = url_match.group(1) if url_match else ""
        content = content_match.group(1).strip() if content_match else ""

        # Append the extracted information as a JSON object to the articles list
        articles.append({
            "title": title,
            "publication_title": publication_title,
            "publication_date": publication_date,
            "ISSN": issn,
            "document_ID": document_id,
            "URL": url,
            "content": content
        })

    # Return the structured data
    return articles

file_path = 'output2.txt' 
articles_json = parse_document(file_path)

# Save the JSON data to a file
with open('parsed_articles2.json', 'w', encoding='utf-8') as json_file:
    json.dump(articles_json, json_file, indent=4, ensure_ascii=False)

print("JSON file has been created successfully.")

