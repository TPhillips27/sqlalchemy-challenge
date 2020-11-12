import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd

#Create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflect database
Base=automap_base() 

#Reflect tables
Base.prepare(engine, reflect=True)

#Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

#Create session linke from Python to the database
session = Session(engine)

#create app
app = Flask(__name__)

#define route/endpoint
@app.route("/")
def index():
    return """
        List all available api routes:<br/>
        /api/v1.0/precipitation<br/>
        /api/v1.0/stations<br>
        /api/v1.0/tobs<br>
        /api/v1.0/<start>yyyy-mm-dd<br>
        /api/v1.0/<start><end>yyyy-mm-dd/yyyy-mm-dd<br/>
    """

start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Retrieve last 12 months of precipitation data
    results = session.query(measurement.date, measurement.prcp).\
                filter(measurement.date > start_date).all()
          
    prcp_data = []
    for date, prcp in results:
        prcp_data_dict = {}
        prcp_data_dict['date'] = date
        prcp_data_dict['prcp'] = prcp
        prcp_data.append(prcp_data_dict)
    
    return jsonify(prcp_data)

@app.route('/api/v1.0/stations')
def stations():
    #Return a JSON list of stations from the dataset.
    results = session.query(Station).all()

    stations = []
    for station in results:
        stations_dict = {}
        stations_dict['Station'] = station 
        stations_dict['Name'] = name
        stations.append(station_dict)

    return jsonify(stations)

#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route('/api/v1.0/tobs')
def tobs():
    
    results = session.query(measurement.station, measurement.date, measurement.tobs)
      
    tobs_data = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict['Station'] = station 
        tobs_dict['Dates'] = date
        tobs_dict['Temp'] = tobs
        tobs_data.append(tobs_dict)

    return jsonify(tobs_data)

#Return a JSON list of the minimum temperature, the average temperature, 
    #and the max temperature for a given start or start-end range.

#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all 
    #dates greater than and equal to the start date.

#When given the start and the end date, calculate the `TMIN`, `TAVG`, 
    #and `TMAX` for dates between the start and end date inclusive.

@app.route('/api/v1.0/<start>')
def start_data(start=None):

    results = session.query(fun.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
                filter(measurement.date >= start).all()

    temp_stats = []

    for Tmin, Tmax, Tavg in results:
        temp_dict = {}
        temp_dict['Min Temp'] = Tmin
        temp_dict['Max Temp'] = Tmax
        temp_dict['Avg Temp'] = Tavg
        temp_stats.append(temp_dict)

    return jsonify(temp_stats)

@app.route("/api/v1.0/temp/<start>/<end>")
def calc_stats(start=None, end=None):
    """Return a json list of the minimum temperature, the average temperature, 
    and the max temperature for a given start-end date range."""
    
    # Query all the stations and for the given range of dates. 
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end).all()

  
    begin_end_stats = []
    
    for Tmin, Tmax, Tavg in results:
        begin_end_stats_dict = {}
        begin_end_stats_dict["Minimum Temp"] = Tmin
        begin_end_stats_dict["Maximum Temp"] = Tmax
        begin_end_stats_dict["Average Temp"] = Tavg
        begin_end_stats.append(begin_end_stats_dict)
    
    return jsonify(begin_end_stats)

# # look at activity 7, 10 for wording 
# # look at titanic 
# # look at 11 for looping 

# #final item
if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port = 5000)


