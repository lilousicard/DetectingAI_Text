from openai import OpenAI
from mongo_utils import get_mongo_client

# Initialize the OpenAI client
client = OpenAI()

# Initialize the MongoDB Atlas Connection
username = 'lilousicardnoel'
cluster_url = 'cluster0.figrf53.mongodb.net'
db_name = 'newsArticle'

mongo_client = get_mongo_client(username, cluster_url, db_name)
db = mongo_client[db_name]
collection = db['topicsForAI']

def generate_article(topic):
    message_content = f"""
        Write a detailed news article about {topic}. 
        Assume you are a New York Times reporter who just heard of the news. 
        Format the output as follows: 
        - Title: write the title 
        - Content: write the content
        Make your output easy to parse into my database.
        Make the articles be at least 500 words.
        """

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": message_content.strip()},
            {"role": "user", "content": topic}
        ]
    )
    return completion.choices[0].message.content

def save_article(topic, article_content):
    filename = topic.replace(' ', '_').lower() + '.txt'
    with open("result.txt", 'a') as file:
        file.write(article_content)
        file.write("\n************************\n")

def retrive_topic():
    lines = []
    query = {}
    for doc in collection.find(query):
        if 'line' in doc:
            lines.append(doc['line'])
    return lines

def main():
    topics = retrive_topic()
    count = 0
    for topic in topics:
        #article_content = generate_article(topic)
        #save_article(topic, article_content)
        print(f"Article on '{topic}' saved to file.")
        count += 1
    print("total: "+ str(count))

if __name__ == '__main__':
    main()

