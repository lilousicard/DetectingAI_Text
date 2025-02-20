import os
from mongo_utils import get_mongo_client
from nltkParser import words_to_pos_types 

username = 'lilousicardnoel'
cluster_url = 'cluster0.figrf53.mongodb.net'
db_name = 'newsArticle'

client = get_mongo_client(username, cluster_url, db_name)
db = client[db_name]
collection = db['ChatGPT-Articles']

try:
    # Process each document in the collection
    for article in collection.find():
        # Check if 'wordFamilyContent' field already exists
        if 'wordFamilyContent' in article:
            continue  # Skip this document
        # Extract the content field from the article
        content = article.get('Content', '')
        # Process the content through nltkParser to get word families
        word_family_content = words_to_pos_types(content)

        # Update the document with the new field 'wordFamilyContent'
        collection.update_one({'_id': article['_id']}, {'$set': {'wordFamilyContent': word_family_content}})

    print("Processing and updating completed successfully.")
except Exception as e:
    print("An error occurred:", e)
