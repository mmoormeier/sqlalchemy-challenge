import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
#Passenger = Base.classes.passenger

Measurement = Base.classes.measurement

Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

@app.route("/")
def welcome():
       return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate/<start><br/>"
        f"/api/v1.0/startenddate/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including date, prcp"""
    # Query all measurements
 
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date <= '2017-08-23').\
    filter(Measurement.date > '2016-08-23').\
    order_by(Measurement.date).all()
      
    session.close()

    # Create a dictionary from the row data and append to a list of all measurements
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[f"{date}"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def priorprecipitation():
     # Create our session (link) from Python to the DB
    session = Session(engine)

#     """Return a list of precipitation data including date, prcp"""
    
    results = session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date <= '2016-08-23').\
    filter(Measurement.date > '2015-08-23').\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date).all()
      
    session.close()
    
  
#     # Create a dictionary from the row data and append to a list of measurments
    prior_precipitation = []
    for date, prcp, station in results:
        prior_precipitation_dict = {}
        prior_precipitation_dict["date"] = date
        prior_precipitation_dict["prcp"] = prcp
        prior_precipitation_dict["station"] = station
        prior_precipitation.append(prior_precipitation_dict)

   
    return jsonify(prior_precipitation)

@app.route("/api/v1.0/startdate/<start>")
def tempstart(start):
    
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).order_by(Measurement.date.desc()).all()
   
    for temps in results:
        dict = {"Minimum Temp":results[0][0],"Average Temp":results[0][1],"Maximum Temp":results[0][2]}
       
    return jsonify(dict) 


@app.route("/api/v1.0/startenddate/<start>/<end>")
def tempstartend(start,end):
    
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
                  filter(Measurement.date >= start, Measurement.date <= end).order_by(Measurement.date.desc()).all()
    
    for temps in results:
        dict = {"Minimum Temp":results[0][0],"Average Temp":results[0][1],"Maximum Temp":results[0][2]}
    return jsonify(dict)   


if __name__ == '__main__':
    app.run(debug=True)