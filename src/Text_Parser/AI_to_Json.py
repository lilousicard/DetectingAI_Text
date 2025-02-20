import json

def parse_file_to_json(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        content = file.read()

    sections = content.strip().split("\n************************\n")
    articles = []

    for section in sections:
        article_data = {}
        lines = section.split('\n')

        for line in lines:
            if line.startswith('Topic:'):
                article_data['Topic'] = line[len('Topic: '):].strip()
            elif line.startswith('Model Used:'):
                article_data['Model Used'] = line[len('Model Used: '):].strip()
            elif line.startswith('Title:'):
                article_data['Title'] = line[len('Title: '):].strip()
            elif line.startswith('Content:'):
                content_index = lines.index(line)
                article_data['Content'] = '\n'.join(lines[content_index + 1:]).strip()

        articles.append(article_data)

    # Write the JSON data to the output file
    with open(output_filename, 'w') as outfile:
        json.dump(articles, outfile, indent=4)

# Usage
input_filename = 'result.txt'  
output_filename = 'output.json'  
parse_file_to_json(input_filename, output_filename)

