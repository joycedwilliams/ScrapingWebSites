# import necessary libraries
from flask import Flask, render_template, redirect

import pymongo

# create instance of Flask app
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

database = client.surfs_db

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    forecasts = database.surf_spots.find({})

    # return template and data
    return render_template("index.html", forecasts=forecasts)


if __name__ == "__main__":
    app.run(debug=True)