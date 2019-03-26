from flask import Flask, render_template, redirect, jsonify, request
from flask_pymongo import PyMongo
import pandas as pd
import pymongo
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
import pprint



# app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder="")
# setup mongo connection

# mongo = PyMongo(app, uri="mongodb://localhost:27017/air_bnb")
uri="mongodb://localhost:27017/air_bnb"
client = MongoClient(uri,
                     connectTimeoutMS=30000,
                     socketTimeoutMS=None,
                     socketKeepAlive=True)

db = client.get_default_database()
print(db.collection_names)
# db = client.air_bnb

# connect to mongo db and collection
collection1 = db["listings"]

collection = db.neighborhoods

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    listings_info = db.listings.find_one()
    return render_template("index.html", data=listings_info)


@app.route("/names")
def names():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
   
    data = pd.DataFrame(list(collection.find({})))

    # Return a list of the column names (sample names)
    return jsonify(list(data.neighbourhood))

@app.route("/listings/<name>")
def listings(name):

   

    data1 = {}
    myquery = {"neighbourhood":{ "$eq": (name) }}
    for listing in collection1.find(myquery):
        data1.update({'id':listing['id'],
        'host_id':listing['host_id'],
        'Host_Name': listing['host_name'],
        'Description':listing['name'],
        'Neighborhood':listing['neighbourhood'],
        'Latitude':listing['latitude'],
        'Longitude': listing['longitude'],
        'Room_Type': listing['room_type'],
        'Price':listing['price'],
        'Minimum_Stay':listing ['minimum_nights'],
        'Number_Reviews':listing['number_of_reviews'],
        'Most_Recent_Review':listing['last_review'],
        'Reviews_per_month':listing['reviews_per_month'],
        'Availability':listing['availability_365']
        })
    print(data1)
    return jsonify(data1)
   


if __name__== '__main__':
    app.run(debug=True)