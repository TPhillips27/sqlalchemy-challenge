import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///./Resources/hawaii.sqlite")
Base=automap_base() 
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station

#create app
app = Flask(__name__)

#define route/endpoint
@app.route("/")
def index():
    return """
        List all available api routes:<br/>
        /api/v1.0/precipitation<br/>
    """
    list everything in one
# 127.0.0.1:5000/.....
# " "/2016-08-23
@app.route("/api/v1.0/precipitation")
# look at activite 7, 10 for wording 
# look at titanic 
# look at 11 for looping 


#final item
if __name__ == '__main__':
    app.run(debug=True)



