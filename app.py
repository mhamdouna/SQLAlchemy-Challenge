# Imports and setup
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Week_10/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


#################################################
# Weclome route
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature for one year: /api/v1.0/tobs<br/>"
        f"Temperature stat from the start date(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temperature stat from start to end dates(yyyy-mm-dd): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )



#################################################
# Precipitation route
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement dates and pcrp values"""
    # Query date and prcp from Measurement
    latest_entry = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(latest_entry, '%Y-%m-%d')
    query_date = dt.date(latest_date.year -1, latest_date.month, latest_date.day)
    precipitation_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of precipitation
    precipitation_list= []
    for date, prcp in precipitation_results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)

# Jsonify list
    return jsonify(precipitation_list)


#################################################
# Stations route
#################################################

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station"""
    # Query station from Station
    station_results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    stations_list= []
    for station, name in station_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name

        stations_list.append(station_dict)

# Jsonify list
    return jsonify(stations_list)


#################################################
# TOBS route
#################################################

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station"""
    # Query dates and tobs values 
    latest_entry = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    latest_date = dt.datetime.strptime(latest_entry, '%Y-%m-%d')
    query_date = dt.date(latest_date.year -1, latest_date.month, latest_date.day)

    sel = [Measurement.station, func.count(Measurement.station)]
    active_station = session.query(*sel).group_by(Measurement.station).order_by(desc(func.count(Measurement.id))).first()[0]

    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).filter(Measurement.station == active_station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of stations
    tobs_list= []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs

        tobs_list.append(tobs_dict)

# Jsonify list
    return jsonify(tobs_list)


#################################################
# Start date route
#################################################

@app.route("/api/v1.0/<start>")
def startdate(start):

 # Create our session (link) from Python to the DB
    session = Session(engine)

# Query min, avg, and max tobs from start date
    start_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()

    session.close()

# Create a dictionary from the row data and append to a list of stations
    startdate_list = []
    for min, max, avg in start_results:
        startdate_dict = {}
        startdate_dict["min"] = min
        startdate_dict["max"] = max
        startdate_dict["avg"] = avg

        startdate_list.append(startdate_dict)

# Jsonify list
    return jsonify(startdate_list)


#################################################
# Start and end dates route
#################################################

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

 # Create our session (link) from Python to the DB
    session = Session(engine)

# Query min, avg, and max tobs from start date to end date
    start_end_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

# Create a dictionary from the row data and append to a list of stations
    start_end_date_list = []
    for min, max, avg in start_end_results:
        start_end_date_dict = {}
        start_end_date_dict["min"] = min
        start_end_date_dict["max"] = max
        start_end_date_dict["avg"] = avg

        start_end_date_list.append(start_end_date_dict)

# Jsonify list
    return jsonify(start_end_date_list)


# Debugger initiation
if __name__ == '__main__':
    app.run(debug=True)
