from pymongo import MongoClient
from mongo_utils import get_mongo_client
import json

# Initialize the MongoDB Atlas Connection
username = 'lilousicardnoel'
cluster_url = 'cluster0.figrf53.mongodb.net'
db_name = 'newsArticle'

mongo_client = get_mongo_client(username, cluster_url, db_name)
db = mongo_client[db_name]
collection = db['NYTimeArticle']

json_file_path = "parsed_articles.json"

try:

    # Load the JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Check if data is a list of documents or a single document
    if isinstance(data, list):
        # Insert multiple documents if it's a list
        collection.insert_many(data)
        print(f"Inserted {len(data)} documents.")
    else:
        # Insert a single document if it's not a list
        collection.insert_one(data)
        print("Inserted one document.")
except Exception as e:
    print(f"An error occurred: {e}")


