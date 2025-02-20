import os
from pymongo import MongoClient

def get_mongo_client(username, cluster_url, db_name, password_env_var='MONGODB_ATLAS_PASSWORD'):
    password = os.getenv(password_env_var)
    if not password:
        raise Exception(f"{password_env_var} environment variable not set")

    connection_uri = f"mongodb+srv://{username}:{password}@{cluster_url}/{db_name}?retryWrites=true&w=majority"
    client = MongoClient(connection_uri)
    return client

