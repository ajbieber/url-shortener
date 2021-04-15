from flask import Flask
from flask import abort, request, render_template
import db
import random
import sys

app = Flask(__name__)
urls = db.connect('localhost', 27017)

@app.route('/')
def hello_world():
    return render_template('url.html')

@app.route('/url', methods=['GET', 'POST'])
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

        if found_doc is None:
            about(404)
        else:
            return found_doc['_id']



def shorten():
    found_doc = true
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

def base_62_encode(n):
    base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    encoded = []

    # Base case
    if n == 0:
        return '0'
    
    while n != 0:
        r = n % 62
        encoded.append(base62[r])
        n = n // 62

    return ''.join(encoded)

    