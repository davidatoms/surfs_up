# Import Flask / Had to create a new env and add Flask to the project
# Set up the Flask Weather app
import datetime as dt
import numpy as np
# Set up Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from flask import Flask
from sqlalchemy import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#   return 'Hello world'

################
# Database Setup
################
# https://stackoverflow.com/questions/33055039/using-sqlalchemy-scoped-session-in-theading-thread
engine = engine = sqlalchemy.create_engine("sqlite://///Users/davidadams/pycharmprojects/module_9/Resources/hawaii.sqlite")

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

##############
# Flask Routes
##############
# Home Route
@app.route("/")
def welcome():
    return """<html>
<h1>Hawaii Traveling Climate App (Flask API)</h1>
<img src="https://www.fodors.com/wp-content/uploads/2018/11/38_GoList_NorthAmerica_Hawaii_shutterstock_339637010.jpg" alt="Hawaii Weather">
<p>Precipitation Analysis:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Station Analysis:</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperature Analysis:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
</ul>
<p>Start & End Day Analysis:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
</ul>
</html>
"""

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   return

# Station Route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
        # Query for the Dates and Temperature Observations from a Year from the Last Data Point
        one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
        # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
        tobs_data = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        tobs_data_list = list(tobs_data)
        # Return JSON List of Temperature Observations (tobs) for the Previous Year
        return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_day_list = list(start_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start Range
        return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return jsonify(start_end_day_list)

# Define Main Behavior
if __name__ == '__main__':
    app.run(debug=True)