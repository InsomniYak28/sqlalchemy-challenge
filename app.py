# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine(r"sqlite:///C:\Users\MichaelaJohnson\OneDrive\Desktop\Edu\challenges\SQLalchemy_challenge\Starter_Code\Starter_Code\Resources\hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

session = Session(bind=engine)

# Save references to each table
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
    print("Server requesting welcome")
    return (
        f"Welcome to the Hawaii Climate Homepage<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/end")

@app.route("/api/v1.0/precipitation")
def precipitation():
    results_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= dt.date(2016, 8, 23)).all()
    session.close()
    prcp_list = []
    for date, prcp in results_prcp:
        prcp_dict= {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
        #List of precipitation data from 2016-8-23 to 2017-8-23
    return jsonify(prcp_list)

@app.route("/api/v1.0/station")
def station():
    results_station = session.query(Station.station).all()
    session.close()
    stations = list(np.ravel(results_station))
    #List of all Stations
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results_tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= dt.date(2016, 8, 23)).all()
    session.close()
    temp_list = []
    for date, tobs in results_tobs:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    #List of temperatures for Station USC00519281 from 2016-8-23 to 2017-8-23
    return jsonify(temp_list)

@app.route("/api/v1.0/start")
def start():
    sel = (Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
    results_start = session.query(*sel).filter(Measurement.date == dt.date(2010, 1, 1)).order_by(Measurement.date).all()
    session.close()
    start_data = list(np.ravel(results_start))
    #Min, Average, and Max temperature data from 2010-01-01
    return jsonify(start_data)

@app.route("/api/v1.0/end")
def end():
    sel = (Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
    results_end = session.query(*sel).filter(Measurement.date == dt.date(2017, 8, 23)).order_by(Measurement.date).all()
    session.close()
    end_data = list(np.ravel(results_end))
    #Min, Average, and Max temperature data from 2017-08-23
    return jsonify(end_data)

if __name__ == "__main__":
    app.run(debug=True)