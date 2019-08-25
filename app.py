from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")
mongo.db.mars.drop()

@app.route("/")
def home():
    mars = mongo.db.mars
    return render_template("index.html", mars =  mars.find_one())

@app.route("/scrape")
def scrape_button():
    mongo.db.mars.drop()
    results = scrape_mars.scrape_results()
    mars= mongo.db.mars
    mars.update({}, results, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)