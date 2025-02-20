import sys
import re

def preprocess_text(text):
    """Preprocess the text to clean and prepare for parsing."""
    # Replace non-breaking spaces and other common anomalies
    text = text.replace('\xa0', ' ').replace('\u2013', '-').strip()
    return text

def split_into_documents(file_content):
    """Split the file content into individual documents based on a specific pattern."""
    pattern = r'Document \d+ of \d+'
    document_starts = [match.start() for match in re.finditer(pattern, file_content)]
    return [file_content[document_starts[i]:document_starts[i + 1] if i + 1 < len(document_starts) else len(file_content)].strip() for i in range(len(document_starts))]

def parse_document(document_raw, wanted_keys, unwanted_keys):
    document = {}
    current_key = None
    lines = document_raw.split('\n')
    
    for line in lines:
        line = preprocess_text(line)
        # Identify potential keys more accurately, considering ':' might appear in normal text
        if ':' in line and not line.startswith((' ', '\t')) and len(line.split(':', 1)[0]) < 40:  # Limit on key length to avoid false positives
            potential_key, value = line.split(':', 1)
            potential_key = potential_key.strip()

            if potential_key in wanted_keys:
                current_key = potential_key
                document[current_key] = value.strip()
            elif potential_key not in unwanted_keys:
                # Reset current_key if the line does not contain a wanted or unwanted key
                current_key = None
        elif current_key:
            # Append line to the existing key, ensuring it doesn't mistakenly capture unwanted content
            document[current_key] += ' ' + line

    return document

def printInFile(parsed_documents, output_filename):
    """Write parsed documents to a file."""
    with open(output_filename, 'w') as file:  # Changed 'a' to 'w' to overwrite and ensure fresh output
        for doc in parsed_documents:
            for key, value in doc.items():
                file.write(f'{key}: {value}\n')
            file.write('\n**************************************************\n\n')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No input file path provided.")
        sys.exit(1)

    filename = sys.argv[1]

    wanted_keys = ["Full text", "Company / organization", "Title", "Publication title", "Publication date", "ISSN", "ProQuest document ID", "Document URL"]
    unwanted_keys = ["Links", "Abstract", "Business indexing term", "First page", "Publication year", "Section", "Publisher", "Place of publication", "Country of publication", "Publication subject", "Source type", "Language of publication", "Document type", "Copyright", "Full text availability", "Last updated", "Database"]

    with open(filename, 'r') as file:
        file_content = file.read()

    document_texts = split_into_documents(file_content)
    parsed_documents = [parse_document(doc, wanted_keys, unwanted_keys) for doc in document_texts]

    printInFile(parsed_documents, "output2.txt")



