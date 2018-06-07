# import libraries
from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape_data

# create instance of Flask app
app = Flask(__name__)

#Function to connect to MongoDB
def connectDB():
    # setup mongo connection
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    # connect to mongo db and collection
    db = client.mars_db
    collection = db.mars_col

    return collection

# route that renders index.html template and finds Mars info from MongoDB
@app.route("/")
def home():
    collection = connectDB()

    # Find data
    mars_info = collection.find_one()

    # return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that trigger scrape functions
@app.route("/scrape")
def scrape():
    collection = connectDB()
    # Run scraped functions
    mars = scrape_data()
    collection.update({"name": "Mars"}, {"$set": mars}, upsert = True)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run()
