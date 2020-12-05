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
   Nu_station = session.query(Station.station).count()
   return jsonify(Nu_stations)


@app.route("/api/v1.0/tobs")
# Return a JSON list of temperature observations (TOBS) for the previous year.
def most_active_station(): 
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= prev_year).all()

    return jsonify(temp_results)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end):
# Return a JSON list of the min, avg  and the max temp for a given start or start-end range.
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:

#calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

        results_temps = session.query(*sel).\
            filter(Measurement.date >= start).all()
        return jsonify(results_temps)

# calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

    results_end = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(results_end)

if __name__ == '__main__': 
    app.run(debug=True)

    session.close()