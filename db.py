from pymongo import MongoClient

# Connect to the database
def connect(host, port):
    # Connect to mongo
    client = MongoClient(host, port)

    # Get the database or create if does not exist
    db = client["urlshortener"]

    # Get the collection or create if does not exist
    collection = db["url"]

    return collection