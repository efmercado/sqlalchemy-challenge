import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import datetime as datetime
from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify

# Creating engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declaring a base using 'automap_base()'
Base = automap_base()

# Using the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assigning classes to variables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Establishing flask
app = Flask(__name__)

@app.route("/")
def welcome():
    """All available api route:"""
    return(
        f"List all available api routes: "
        f" <br/><br/>"
        f"/api/v1.0/precipitation <br/><br/>"
        f"/api/v1.0/stations <br/><br/>"
        f"/api/v1.0/tobs <br/><br/>"
        f"/api/v1.0/<start> <br/>"
        f"Add a Start date to the end using the format 'Y-m-d' <br/>"
        f"Example: /api/v1.0/2016-08-12<br/><br/>"
        f"/api/v1.0/<start>/<end><br/>"
                f"Add a Start date to the second to last '/' and End date at the end using the format 'Y-m-d' <br/>"
        f"Example: /api/v1.0/2016-08-12/2016-08-17"
    )

# --------------------------------------------
# First Route
# --------------------------------------------

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Creating a session from Python to the DB
    session = Session(engine)
    
    # Querying all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    precipitation_data = []
    for date, prcp in results:
        precipitation_dict = {str(date):str(prcp)}
        precipitation_data.append(precipitation_dict)
        
    return jsonify(precipitation_data)

# ----------------------------------------------
# Second Route
# ----------------------------------------------

@app.route("/api/v1.0/stations")
def stations():
    # Create session from Python to the DB
    session = Session(engine)
    
    # Query all precipitation data
    results = session.query(Station.station, Station.name).all()
    
    
    session.close()
    
    station_data = []
    for station, name in results:
        station_dict = {}
        station_dict['Station ID'] = station
        station_dict['Station Name'] = name
        station_data.append(station_dict)
        
    return jsonify(station_data)
    
    
# --------------------------------------------
# Third Route
# --------------------------------------------

@app.route('/api/v1.0/tobs')
def tobs():
    # Create session from Python to the DB
    session = Session(engine)
    
    # Latest date
    latest_measurement_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = datetime.datetime.strptime(latest_measurement_date[0], '%Y-%m-%d').date()
    
    # Date 12 months ago
    last_12_months  = latest_date - relativedelta(months = 12)
    
    # Query for temperature in the last 12 months
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_12_months).all()
    
    session.close()
    
    temperature_data = []
    for date, tobs in results:
        temperature_dict = {}
        temperature_dict["Date"] = date
        temperature_dict["Temperature"] = tobs
        temperature_data.append(temperature_dict)
        
    return jsonify(temperature_data)


# --------------------------------------------
# Fourth Route
# --------------------------------------------


@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create session from Python to the DB
    session = Session(engine)
    
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
                                      func.avg(Measurement.tobs)).\
                                      filter(Measurement.date >= start_date).all()
    
    temp_stats_results = list(np.ravel(temperature_stats))
    
    min_temp = temp_stats_results[0]
    max_temp = temp_stats_results[1]
    avg_temp = temp_stats_results[2]
                                      
    temp_stats_data = []
    temp_stats_dict = [{"Start Date": start},
                       {"Minimum Temperature": min_temp},
                       {"Maximum Temperature": max_temp},
                       {"Average Temperature": avg_temp}]

    temp_stats_data.append(temp_stats_dict)
    
    return jsonify(temp_stats_data)                                  

# --------------------------------------------
# Fifth Route
# --------------------------------------------
@app.route('/api/v1.0/<start>/<end>')                                    
def start_end_date(start, end):
    # Create session from Python to the DB
    session = Session(engine)
    
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),
                                      func.avg(Measurement.tobs)).\
                                      filter(Measurement.date >= start_date).\
                                      filter(Measurement.date <= end_date).all()
    
    temp_stats_results = list(np.ravel(temperature_stats))
    
    min_temp = temp_stats_results[0]
    max_temp = temp_stats_results[1]
    avg_temp = temp_stats_results[2]
    
    temp_stats_data = []
    temp_stats_dict = [{"Start Date": start_date},
                       {"End Date": end_date},
                       {"Minimum Temperature": min_temp},
                       {"Maximum Temperature": max_temp},
                       {"Average Temperature": avg_temp}]

    temp_stats_data.append(temp_stats_dict)
    
    return jsonify(temp_stats_data)


# --------------------------------------------

if __name__ == '__main__':
    app.run(debug = True)                                 