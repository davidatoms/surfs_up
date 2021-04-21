# Import Flask / Had to create a new env and add Flask to the project
# Set up the Flask Weather app
import datetime as dt
import numpy as np
import re
# Set up Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from flask import Flask, jsonify
from sqlalchemy import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists

################
# Database Setup
################
# https://stackoverflow.com/questions/33055039/using-sqlalchemy-scoped-session-in-theading-thread
engine = sqlalchemy.create_engine(
    "sqlite://///Users/davidadams/pycharmprojects/module_9/Resources/hawaii.sqlite")

# Reflect Existing Database Into a New Model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save References to Each Table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create Session (link) from Python to the database
session = Session(engine)

#############
# Flask Setup
#############
app = Flask(__name__)

latestDate = (session.query(Measurement.date)
                .order_by(Measurement.date.desc())
                .first())
latestDate = list(np.ravel(latestDate))[0]

latestDate = dt.datetime.strptime(latestDate, '%Y-%m-%d')
latestYear = int(dt.datetime.strftime(latestDate, '%Y'))
latestMonth = int(dt.datetime.strftime(latestDate, '%m'))
latestDay = int(dt.datetime.strftime(latestDate, '%d'))

yearBefore = dt.date(latestYear, latestMonth, latestDay) - dt.timedelta(days=365)
yearBefore = dt.datetime.strftime(yearBefore, '%Y-%m-%d')

##############
# Flask Routes
##############
# Home Route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )


# Convert query results to a dictionary using `date` as the key and `tobs` as the value
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session.query(Measurement.date, Measurement.prcp). \
        filter(Measurement.date >= prev_year).all()
    return


# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)


# Query the dates and temperature observations of the most active station for the last year of data
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)



# Calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run(debug=True)
