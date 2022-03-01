#dependencies
from distutils.log import debug
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

inspector = inspect(engine)
inspector.get_table_names()

#flask setup
app = Flask(__name__)

#home route
@app.route("/")
def home():
    return("/api/v1.0/precipitation<br/>"
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/<start><br/>"
    "/api/v1.0/<start>/<end><br/>"
    )

#precipitation route
@app.route("/api/v1.0/precipitation")
def percipittion():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year).\
        order_by(Measurement.date).all()
    list_prcp_data = dict(prcp_data)
    return jsonify(list_prcp_data)

#station route
@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.station, Station.name).all()
    list_stations = list(all_stations)
    return jsonify(list_stations)

#tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= one_year).\
        order_by(Measurement.date).all()
    list_tobs_data = list(tobs_data)
    return jsonify(list_tobs_data)

#start date route
@app.route("/api/v1.0/<start>")
def start_date(start):
    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        group_by(Measurement.date).all()
    list_start_date = list(start_date)
    return jsonify(list_start_date)

#start & end date route
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    start_end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        group_by(Measurement.date).all()
    list_start_end_date = list(start_end_date)
    return jsonify(list_start_end_date)

if __name__ == '__main__':
    app.run(debug=True)


