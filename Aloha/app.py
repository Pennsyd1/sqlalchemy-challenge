from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
    # Query data

    mes =[Measurement.prcp, Measurement.date]
    results = session.query(*mes).\
    filter(func.strftime(Measurement.date) >= "2016-08-23").\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_data = []
    for prcp, date in results:
        prcp_dict = {}
        prcp_dict["prcp"] = prcp
        prcp_dict["date"] = date
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)



@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    mes_tobs =[Measurement.date, Measurement.tobs]
    results = session.query(*mes_tobs).\
    filter(func.strftime(Measurement.date) >= "2016-08-23").\
    group_by(Measurement.tobs).\
    order_by(Measurement.tobs).all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    """Fetch the list of the minimum temperature, 
    the average temperature, and the maximum temperature for a specified start or start-end range."""
    temps = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp = session.query(*temps).\
        filter(Measurement.date >= start).all()
    print(temp)
    return jsonify(temp)


if __name__ == '__main__':
    app.run(debug=True)
