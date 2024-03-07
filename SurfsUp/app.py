# Import the dependencies.
from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session_var = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home_page():
    """List all available api routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the last 12 mos of precip data
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    
    session.close()

    # Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)
    # to a dictionary using date as the key and prcp as the value.
    precip_analysis = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_analysis.append(precip_dict)

    # Return the JSON representation of your dictionary.
    return jsonify(precip_analysis)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for all stations in the database
    results = session.query(Measurement.station).distinct().all()
    
    session.close()
    
    # Crete a dictionary of all stations
    all_stations = []
    for name in results:
        stations_dict = {}
        stations_dict["name"] = name[0]
        all_stations.append(stations_dict)

    # Return a JSON list of stations from the dataset.
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the dates and temperature observations of the most-active station for the previous year of data.
    results = session.query(Measurement.date, Measurement.tobs).filter((Measurement.station == 'USC00519281') & (Measurement.date >= '2016-08-23')).all()
    
    session.close()

   # Create a dictionary of tobs data
    tobs_data = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_data.append(tobs_dict)

    # Return a JSON list of temperature observations for the previous year.
    return jsonify(tobs_data)


@app.route("/api/v1.0/<start>")
def temp_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the minimum temp, average temp, and the maximum temp for a specified start date (as a parameter from the URL)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close()

    temp_data = []
    for tobs in results:
        temp_dict = {}
        temp_dict["Minimum"] = tobs[0]
        temp_dict["Maximum"] = tobs[1]
        temp_dict["Average"] = tobs[2]
        temp_data.append(temp_dict)


    return jsonify(temp_data)


@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query the minimum temp, average temp, and the maximum temp for a specified start date to a specified end date (as parameters from the URL)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter((Measurement.date >= start)&(Measurement.date <= end)).all()
    
    session.close()

    temp_data = []
    for tobs in results:
        temp_dict = {}
        temp_dict["Minimum"] = tobs[0]
        temp_dict["Maximum"] = tobs[1]
        temp_dict["Average"] = tobs[2]
        temp_data.append(temp_dict)

    return jsonify(temp_data)

if __name__ == "__main__":
    app.run(debug=True)