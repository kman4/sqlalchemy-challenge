import pandas as pd
import sqlalchemy
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify

# Database Setup

engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup

app = Flask(__name__)

# Flask Routes

@app.route("/")
def main():    
    return "Welcome to Hawaii API!"

@app.route("/api/v1.0/precipitation")
def precipitation(): 
    oneyr_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= oneyr_ago).order_by(Measurement.date).all()
    results = {date:prcp for date,prcp in one_year}
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations(): 
# Design a query to show how many stations are available in this dataset?
    session.query(Measurement.station).group_by(Measurement.station).count()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def precipitation(): 
    oneyr_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    one_year = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= oneyr_ago).order_by(Measurement.date).all()
    results = {date:prcp for date,prcp in one_year}
    return jsonify(results)

if __name__ == '__main__': 
    app.run(debug=True)