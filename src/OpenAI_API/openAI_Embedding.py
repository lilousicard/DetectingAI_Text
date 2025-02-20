from openai import OpenAI
from pymongo import MongoClient
from mongo_utils import get_mongo_client

# Initialize the MongoDB Atlas Connection
username = 'lilousicardnoel'
cluster_url = 'cluster0.figrf53.mongodb.net'
db_name = 'newsArticle'

mongo_client = get_mongo_client(username, cluster_url, db_name)
db = mongo_client[db_name]
collections = ['NYTimeArticle', 'ChatGPT-Articles', 'ProQuest-Articles']

client = OpenAI()

for collection_name in collections:
    collection = db[collection_name]
   
    for document in collection.find():
        # Check both 'content' and 'Content' fields
        text = document.get('content') or document.get('Content', '')
        # Generate embeddings for the text, only if text is not empty
        if text:
            response = client.embeddings.create(
                input=text,
                model="text-embedding-3-small"
            )
            embedding = response.data[0].embedding  # Assuming this is the correct structure
            print(embedding)
            # Update the document with the embedding
            collection.update_one(
                {'_id': document['_id']},
                {'$set': {'text-embedding-3-small': embedding}}
            )

print("Embeddings have been stored in the database.")

