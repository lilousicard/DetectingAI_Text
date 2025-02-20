import json
from mongo_utils import get_mongo_client

username = 'lilousicardnoel'
cluster_url = 'cluster0.figrf53.mongodb.net'
db_name = 'newsArticle'

client = get_mongo_client(username, cluster_url, db_name)
db = client[db_name]

collections = ["topicsForAI", "ChatGPT-Articles", "ProQuest-Articles", "NYTimeArticle"]

for collection_name in collections:
    collection = db[collection_name]
    documents = list(collection.find())

    # Print the number of documents retrieved
    print(f"Number of documents in {collection_name}: {len(documents)}")

    with open(f"{collection_name}.json", "w") as file:
        for document in documents:
            file.write(json.dumps(document, default=str) + '\n')

print("Database exported successfully.")