import os

import requests
import time
import webbrowser
from mongo_utils import get_mongo_client

username = 'lilousicardnoel'
cluster_url = 'cluster0.figrf53.mongodb.net'
db_name = 'newsArticle'

mongo_client = get_mongo_client(username, cluster_url, db_name)
db = mongo_client[db_name]
collection = db['topicsForAI']

# get api key from os environment
api_key = os.getenv('NYT_API_KEY')
base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

def retrieve_topic():
    lines = []
    query = {}
    for doc in collection.find(query):
        if 'line' in doc:
            lines.append(doc['line'])
    return lines


def fetch_articles(year, topic, api_key):
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        'q': topic,
        'begin_date': f"{year}0101",
        'end_date': f"{year}1231",
        'api-key': api_key
    }
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching articles: {response.status_code}")
        return {}

topics = retrieve_topic()

# Open a text file to write the output
with open('APIResult.txt', 'w', encoding='utf-8') as file:
    for topic_entry in topics:
        year, topic = topic_entry.split(': ', 1)
        json_response = fetch_articles(year.strip(), topic.strip(), api_key)

        if json_response:
            if 'response' in json_response and 'docs' in json_response['response']:
                file.write(f"Articles for {year}: {topic}\n")
                for article in json_response['response']['docs']:
                    file.write(f"{article['headline']['main']}\n")
                    file.write(f"{article['pub_date']}\n")
                    file.write(f"{article['web_url']}\n")
                file.write("\n" + "-"*80 + "\n\n")
            else:
                file.write(f"Error or unexpected structure in response for {year}: {topic}\n")
        else:
            file.write(f"No response received for {year}: {topic}. Possibly due to a bad request or rate limiting.\n")

        file.flush()
        time.sleep(12)

