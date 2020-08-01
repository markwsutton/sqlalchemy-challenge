#!/usr/bin/env python
# coding: utf-8

# ## Step 2 - Climate App

# In[1]:


# Dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# In[ ]:


# Database Setup
engine = create_engine("sqlite:///./Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[ ]:


# Create session link
session = Session(engine)


# In[ ]:


# Flask Setup
app = Flask(__name__)


# In[ ]:


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii analysis API routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Get 1 year ago date
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(365)

    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # precip
    precip = {date: prcp for date, prcp in results}
    print(precip)
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    
    # Query all stations
    results = session.query(Station.station).all()

    # stations
    stations_data = list(np.ravel(results))
    return jsonify(stations_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Get 1 year ago date
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(365)

    # Query last year for most active station
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_ago).all()

    # temps
    temps = list(np.ravel(results))
    return jsonify(temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end: 
        results = session.query(*sel).filter(Measurement.date >= start).all()

        temps = list(np.ravel(results))
        return jsonify(temps)
    
    # calculate values within dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    # Unravel, convert to list
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


if __name__ == '__main__':
    app.run(debug=True)

