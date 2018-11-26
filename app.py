#########################################
# import packages
#########################################

#basic packages
import os
import pandas as pd
import numpy as np

#sqlalchemy to access sqlite database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

#flask to create server
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

#create flask server
app = Flask(__name__, static_url_path = '')

#########################################
# Database Setup
#########################################

#connect to database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

#reflect existing database into a new model
Base = automap_base()
#reflect the tables
Base.prepare(db.engine, reflect=True)

#save references to each table
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples

###########################################
# Flask Routes
###########################################

#home page
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

#sample names
@app.route("/names")
def names():
    """Return a list of sample names."""

    #Use Pandas to perform the sql query
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    #Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])

#sample metadata for each sample
@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    #choose variables to get
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    #run SQL query
    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    #Create a dictionary entry for each row
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    #print data and jsonify it for access
    print(sample_metadata)
    return jsonify(sample_metadata)

#sample data for each sample
@app.route("/samples/<sample>")
def samples(sample):
    """Reutnr `otu_ids`, `otu_lables`, and `sample_values`."""
    #Create a SQL query and read it into a pandas dataframe.
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    #Filter the data based on the sample number and
    #only keep rows with values above 1
    sampled_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

    #Sort sample_values in descending order
    sample_data = sampled_data.sort_values(by = sample, ascending = False)

    #Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.values.tolist()
    }

    #return jsonify'd data
    return jsonify(data)

##################################################
# Final Code
##################################################

#code to actually run file
if __name__ == "__main__":
    app.run()




