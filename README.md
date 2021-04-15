# url-shortener

This repository contains code for creating a very simplistic URL shortener. It is written in Python
using Flask, and while it does contain an incomplete UI, supports a complete RESTful API. 

The total time spent on this application was roughly 3 hours. About an hour was spent setting up the
base Flask application and getting the MongoDB database up. The next 1.5 hours were spent developing
the actual application. This took a bit longer than I hoped for, due to the face that I had never
developed using Flask before, but chose Flask since it was easy to spin up. The final 0.5 hours were
spent creating thie README and cleaning up code. 

## Recommended Use

As stated above, while a UI does exist, it is incomplete. It is recommended for full functionality to
use the RESTful API. To shorten a url, make a POST request to `http://localhost:5000/api/url`,
cointaining a single form field `url`. I found it easiest to use 
[Postman](https://www.postman.com/downloads/) for this. *Please note, this API does expect form data
and not JSON. This is an improvement I would like to make.* To retrieve an original url, make a GET
request to `http://localhost:5000/api/url`, followed by a query parameter `short`, with the value
being the shortened url.

## Requirements

Before running the application, you will need to ensure you have a running instance of MongoDB,
listening on the default port of 27017. My personal preference was to run Mongo via Docker,
following the instructions found [here](https://hub.docker.com/_/mongo). To start my instance
locally, I ran the command:

```bash
    docker run --name mongo -p 27017:27017 -d mongo:latest
```

## Running the application

To run the application, we will first need to install the required modules. By running the command
`pip install -r requirements.txt`, we can install all the necessary dependencies. Since the
application is a flask application, we will need to export the name of the app by running
`export FLASK_APP=main.py`. Finally after doing this, you can run the application by running
`flask run`. This will start the application on port 5000.

## Improvements
There are many improvements that could be made to this application. The first and foremost is that
the user interface could be improved to better support error handling and retrieval of the original
URL via form submission.

Another area that needs improvement is the database choice. Probably the most optimal database for
this exercise would have been a relational database, since we would only really need to scale
vertically. As this tool is used more and more, countless entries will be added to the database, but
entries will always be roughly the same size. For this reason, it makes sense to use a relational
database.

Finally, the last big improvement would be the algorithm for shortening urls. Due to time
constraints, I chose to implement an algorithm that converted a random number into a base_62 string,
where base_62 contains all numbers, lowercase and uppercase letters. For a lesser used tool, this
option is fine. But as more and more urls are used up, the random number generator may have
collisions, and will take longer and longer to generate a unique random number. Additionally,
there would be a maximum of 9223372036854775807 urls, the value of `sys.maxsize`.