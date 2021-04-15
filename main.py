import random
import sys
from flask import Flask
from flask import abort, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to mongo
client = MongoClient('localhost', 27017)

# Get the database or create if does not exist
db = client['urlshortener']

# Get the collection or create if does not exist
urls = db['url']

# Index the shortened field, _id is already indexed
urls.create_index('shortened')


########################################################
#                                                      #
#                      ROUTES                          #
#                                                      #
########################################################

@app.route('/')
def home():
    return render_template('url.html')

@app.route('/api/url', methods=['GET', 'POST'])
def url():
    if request.method == "POST":
        # Attempt to find a matching document
        found_doc = urls.find_one({'_id': request.form['url']})
        
        # If no document found, proceed with creating shortened url
        if found_doc is None:
            # Shorten the url
            shortened = shorten()

            # Create the document
            url = {
                '_id': request.form['url'],
                'shortened': shortened
            }

            urls.insert_one(url)

            return shortened
        else:
            # Similar document already exists, return 409 Conflict
            abort(409)
    else:
        # Attmept to find the matching url
        short = request.args.get('short')
        found_doc = urls.find_one({ 'shortened': short })

        # If no document was found, return 404
        if found_doc is None:
            about(404)
        else:
            # Return original url
            return found_doc['_id']



########################################################
#                                                      #
#                 HELPER FUNCTIONS                     #
#                                                      #
########################################################

# Returns a randomly generated "shortened" url
def shorten():
    found_doc = True
    short = ''

    # Continue producing random urls until a non-duplicate occurs
    while found_doc is not None:
        # Generate random number between 0 and largest number in system
        a = random.randint(0, sys.maxsize)
        # Encode the number into base62
        short = 'https://byte.ly/' + base_62_encode(a)
        # Search for matching document in db
        found_doc = urls.find_one({'shortened': short})

    return short

# Returns a base62 encoded version of an integer
def base_62_encode(n):
    base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encoded = []

    # Base case
    if n == 0:
        return '0'
    
    # While we can still divide by 62
    while n != 0:
        r = n % 62 # index of character

        # Append character to array
        encoded.append(base62[r])
        n = n // 62

    # Join all characters and return
    return ''.join(encoded)

    