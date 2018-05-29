# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo
from scrape_mars import scrape_data

# create instance of Flask app
app = Flask(__name__)

def connectDB():
    # setup mongo connection
    conn = "mongodb://localhost:27017"
    client = pymongo.MongoClient(conn)

    # connect to mongo db and collection
    db = client.mars_db

    # Drops collection if available to remove duplicates

    collection = db.mars_col
    # create route that renders index.html template and finds documents from mongo
    return collection

@app.route("/")
def home():
    collection = connectDB()

    # Find data
    mars_info = collection.find_one()

    # return template and data
    return render_template("index.html", mars_info=mars_info)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    collection = connectDB()
    # Run scraped functions
    mars = scrape_data()
    collection.update({"name": "Mars"}, {"$set": mars}, upsert = True)
    #print(mars_data)

    # Store results into a dictionary
    #mars_info = {
    #    "news_title": mars["news_title"],
    #    "news_content": mars["news_content"],
    #    "featured_image_url": mars["featured_image_url"],
    #    "mars_weather": mars["mars_weather"],
    #    "mars_facts": mars["mars_facts"],
    #    "hemisphere_images": mars["hemisphere_images"]
    #}

    # Insert forecast into database
    #client.db.collection.insert_one(mars_info)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
