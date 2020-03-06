from flask import Flask, render_template, redirect
from flask_pymongo import Pymongo
import scrape_mars

app = Flask(__name__)
mongo = Pymongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert = True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)