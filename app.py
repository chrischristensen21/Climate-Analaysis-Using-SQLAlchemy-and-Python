import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)
    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter((Measurement.station) == 'USC00519281', (Measurement.date)>=last_year).all()
    session.close()
    
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_date>")
def date_temps(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    session.close()

    all_date_temps = []
    for result in results:
        date_temps_dict = {}
        date_temps_dict["TMIN"] = result[0]
        date_temps_dict["TAVG"] = result[1]
        date_temps_dict["TMAX"] = result[2]
        
        all_date_temps.append(date_temps_dict)
    return jsonify(all_date_temps)
   
@app.route("/api/v1.0/<start_date>/<end_date>")
def range_temps(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()

    all_range_temps = []
    for result in results:
        range_temps_dict = {}
        range_temps_dict["TMIN"] = result[0]
        range_temps_dict["TAVG"] = result[1]
        range_temps_dict["TMAX"] = result[2]
        
        all_range_temps.append(range_temps_dict)
    return jsonify(all_range_temps)

   
if __name__ == '__main__':
    app.run(debug=True)