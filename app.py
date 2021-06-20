import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# declare Base
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        
        f"<h1>Welcome!</h1></br>"
        f"<h2>This API provides climate data for Hawaii</h2></br>"

        f"<h3>Available Routes:</h3><br/>"
        
        f"<b>Returns a JSON list of precipitation measurements.</b></br>"
        f"/api/v1.0/precipitation<br/><br/>"
        
        f"<b>Returns a JSON list of stations from the dataset.</b></br>"
        f"/api/v1.0/stations<br/><br/>"
        
        f'''<b>Returns a JSON list of temperature observations (TOBS) 
        for the previous year.</b></br>'''
        f"/api/v1.0/tobs<br/><br/>"

        f'''<b>Return a JSON list of the max temperatures, 
        min temperatures, and avg temperatures 
        for a given start or start-end range.
        End date is optional.</br>
        Enter dates in format 'YYYY-MM-DD'</b><br/></br>'''
        f"/api/v1.0/start_date</br>"
        f"/api/v1.0/start_date/end_date<br/></br>"
        f"<em>Examples:</em></br>"
        f"/api/v1.0/2017-01-01</br>"
        f"/api/v1.0/2017-01-01/2017-12-31"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation data"""
    # Query precipitation measurments
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # # Convert list of tuples into normal list
    # dates = [results[i][0] for i in range(len(results))]
    # prcp_measures = [results[i][1] for i in range(len(results))]

    return jsonify(dict(results))

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of stations and station names"""
    # Query stations and station names
    results = session.query(Station.station, Station.name).join(Measurement, Station.station == Measurement.station)

    session.close()

    return jsonify(dict(results))

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temperature observations from the most active station for the most recent one-year period"""
    
    # find the most recent date in the data set.
    most_recent_date_str = session.query(func.max(Measurement.date)).first()[0]

    # convert string date to datetime date
    most_recent_date = dt.datetime.strptime(most_recent_date_str, "%Y-%m-%d").date()
    
    # calculate the date one year from the last date in data set.
    year_prior = most_recent_date - dt.timedelta(days=365)
    
    # find the station with the greatest number of measurements
    most_active_station = session.query(Measurement.station, func.count(Measurement.id)).group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).first()[0]

    # Query temperature observations for most recent year
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_prior, Measurement.station == most_active_station)

    session.close()

    return jsonify(dict(results))

@app.route("/api/v1.0/<start>")
def summarize_temp_after_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # find the most recent date in the data set.
    most_recent_date_str = session.query(func.max(Measurement.date)).first()[0]

    # convert string date to datetime date
    most_recent_date = dt.datetime.strptime(most_recent_date_str, "%Y-%m-%d").date()

    """Return min, max, and average temperatures after specifified date (inclusive)"""
    #format start date as datetime date
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    
    # Query data
    results = session.query(func.max(Measurement.tobs).label('temp_max'), func.min(Measurement.tobs).label('temp_min'), func.avg(Measurement.tobs).label('temp_avg')).filter(Measurement.date >= start_date).all()

    session.close()
    
    # Create a dictionary from the data
    temps_list = []
    for temp_max, temp_min, temp_avg in results:
        temps_dict = {}
        temps_dict['start_date'] = str(start_date)
        temps_dict['end_date'] = str(most_recent_date)
        temps_dict["temp_max"] = temp_max
        temps_dict["temp_min"] = temp_min
        temps_dict["temp_avg"] = temp_avg
        temps_list.append(temps_dict)

    return jsonify(temps_list)

@app.route("/api/v1.0/<start>/<end>")
def summarize_temp_between_dates(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return min, max, and average temperatures between specifified dates (inclusive)"""
    #format start date as datetime date
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()
    
    # Query data
    results = session.query(func.max(Measurement.tobs).label('temp_max'), func.min(Measurement.tobs).label('temp_min'), func.avg(Measurement.tobs).label('temp_avg')).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

    session.close()
    
    # Create a dictionary from the data
    temps_list = []
    for temp_max, temp_min, temp_avg in results:
        temps_dict = {}
        temps_dict["start_date"] = str(start_date)
        temps_dict["end_date"] = str(end_date)
        temps_dict["temp_max"] = temp_max
        temps_dict["temp_min"] = temp_min
        temps_dict["temp_avg"] = temp_avg
        temps_list.append(temps_dict)

    return jsonify(temps_list)

if __name__ == '__main__':
    app.run(debug=True)