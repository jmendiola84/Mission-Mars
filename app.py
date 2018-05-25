# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_db

# Drops collection if available to remove duplicates
db.mars_col.drop()
collection = db.mars_col
# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_info = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    mars_data = scrape_mars.scrape_data()


    # Store results into a dictionary
    mars_info = {
        "news_title": mars["news_title"],
        "news_content": mars["news_content"],
        "featured_image_url": mars["featured_image_url"],
        "mars_weather": mars["mars_weather"],
        "mars_facts": mars["mars_facts"],
        "hemisphere_images": mars["hemisphere_images"]
    }

    # Insert forecast into database
    #mongo.db.collection.insert_one(mars_info)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
