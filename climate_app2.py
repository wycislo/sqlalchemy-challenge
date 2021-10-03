import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, render_template , jsonify
import datetime as dt
import json

app = Flask(__name__)



engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


@app.route("/")


@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route("/api/v1.0/precipitaton")
def precipitation():
    return prcp_list

@app.route("/api/v1.0/stations")
def stations():
    return stations_list

@app.route("/api/v1.0/tobs")
def tobs():
    return tobs_list

@app.route("/api/v1.0/<start>")
def given_start(start):
        start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            group_by(Measurement.date).all()
        start_list = list(start_day)
        return start_list

@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
        start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).\
                group_by(Measurement.date).all()
        # Convert List of Tuples Into Normal List
        start_end_day_list = list(start_end_day)
        # Return JSON List of Min Temp, Avg Temp and Max Temp for a Given Start-End Range
        return start_end_day_list


@app.route("/about")
def about():
    return render_template('about.html')



# query precipitation data 
# Find the most recent date in the data set.
earlieststr = session.query(Measurement.date).order_by(Measurement.date).first()
lateststr = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
latestdate = dt.datetime.strptime(lateststr[0], '%Y-%m-%d')
# find the last year of data set.
querydate = dt.date(latestdate.year -1, latestdate.month, latestdate.day)
sel = [Measurement.date,Measurement.prcp]

# convert query result returned as a list
queryresult = session.query(*sel).filter(Measurement.date >= querydate).all()
# convert list to a dictionary
prcp_list = dict(queryresult)

# station data 
# return a list of stations 
stations_all = session.query(Station.station, Station.name).all()
stations_list = dict(stations_all)

# TOBS
# Query the dates and temperature observations of the most active station 
# for the last year of data.

tobs_query = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= querydate).\
        order_by(Measurement.date).all()
tobs_list = dict(tobs_query)   


if __name__=="__main__":
    app.run(debug=True)




