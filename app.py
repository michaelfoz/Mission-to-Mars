# This file created per Module 10.5.1: Use Flask to Create a Web App
# https://courses.bootcampspot.com/courses/1225/pages/10-dot-5-1-use-flask-to-create-a-web-app?module_item_id=498590

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set Up App Routes

# Define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Add the next route and function
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
    app.run()

# -----------(SELF-NOTES BELOW)-----------

# from flask import Flask, render_template, redirect, url_for--->use Flask to render a template, redirecting to another url, and creating a URL
# from flask_pymongo import PyMongo--->use PyMongo to interact with Mongo database
# import scraping--->use the scraping[.py] code (Module 10.3.3-10.3.5), we will convert from Jupyter notebook to Python

# Comment: Set up Flask
# app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"--->Tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
# mongo = PyMongo(app)--->is the URL we'll be using to connect our app to Mongo. This URL is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app."

# Comment: Set Up [2] App Routes:
# (1st route) for the main HTML page everyone will view when visiting the web app
# (2nd route) to actually scrape new data using the code we've written

   # Rewind:
   # Flask routes bind URLs to functions. For example, the URL "ourpage.com/" brings us to the homepage of our web app. 
   # The URL "ourpage.com/scrape" will activate our scraping code.
   # These routes can be embedded into our web app and accessed via links or buttons.

# Comment: 1st App Route: Define the route for the HTML page
# @app.route("/")--->Tells Flask what to display when we're looking at the home page, index.html (index.html is the default HTML file that we'll use to display the content we've scraped). This means that when we visit our web app's HTML page, we will see the home page.

# (Start of function)
# def index():--->(This is a function defined)
#    mars = mongo.db.mars.find_one()--->uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script. We will also assign that path to themars variable for use later.
#    return render_template("index.html", mars=mars)

   # Comment: return render_template("index.html" tells Flask to return an HTML template using an index.html file. We'll create this file after we build the Flask routes.
   # Comment: , mars=mars) tells Python to use the "mars" collection in MongoDB.
# (End of function)

# Comment: 2nd App Route: Add the next route and function--->This route will be the "button" of the web application, the one that will scrape updated data when we tell it to from the homepage of our web app. It'll be tied to a button that will run the code when it's clicked.
# @app.route("/scrape")--->Defines the route that Flask will be using. This route, “/scrape”, will run the function that we create just beneath it.

# Comment: (The next lines allow us to access the database, scrape new data using our scraping.py script, update the database, and return a message when successful.)

# (Start of function)
# def scrape():--->(This is a function defined)
#    mars = mongo.db.mars--->Assign a new variable that points to our Mongo database.
#    mars_data = scraping.scrape_all()--->Create a new variable to hold the newly scraped data. (In this line, we're referencing the scrape_all function in the scraping.py file exported from Jupyter Notebook.)

#    mars.update_one({}, {"$set":mars_data}, upsert=True)--->Now that we've gathered new data, we need to update the database using .update_one().

         # Comment: .update_one(query_parameter, {"$set": data}, options)
         # Here, we're inserting data, but not if an identical record already exists. 
         # In the query_parameter, we can specify a field (e.g. {"news_title": "Mars Landing Successful"}), in which case MongoDB will update a document with a matching news_title. 
         # Or it can be left empty ({}) to update the first matching document in the collection.

         # Next, use the data stored in mars_data. The syntax used here is {"$set": data}. 
         # This means that the document will be modified ("$set") with the data in question.

         # Finally, the option we'll include is upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, 
         # and new data will always be saved (even if we haven't already created a document for it).

         # The entire line of code looks like this: mars.update_one({}, {"$set":mars_data}, upsert=True).

#    return redirect('/', code=302)--->Finally, add a redirect after successfully scraping the data. return redirect('/', code=302) will navigate our page back to [/] where we can see the updated content.
# (End of function)

# The final bit of code (below) is what is needed in order to tell Flask to run.
# if __name__ == "__main__":
#     app.run()