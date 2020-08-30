from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

#Use flask pymongo to set up connection

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" 
mongo = PyMongo(app)

# Or set it inline
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app" 

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"

if __name__ == "__main__":
    app.run()