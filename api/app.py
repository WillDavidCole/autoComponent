"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
from flask import Flask
app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

from flask import  jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from DbConfig.DbConfig import DbConfig

import pyodbc

# Connection
db = DbConfig()
constring = db.connectionString_get() #'DRIVER={SQL Server};Server=PCM-HG79N53;DATABASE=wic_Dream_Snapshot;Trusted_Connection=yes;'
conn = pyodbc.connect(constring)

# Flask app
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % constring
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class RunId(Resource):
    def get(self, RunId):
        cur = conn.cursor()
        all_runs = cur.execute('exec dbo.stp_Calibration_GetRunInputs %d' % RunId ).fetchall()
        results = [tuple(row) for row in all_runs]
        return jsonify(results)

class Runs(Resource):
    def get(self):
        cur = conn.cursor()
        all_runs = cur.execute('SELECT * FROM RunInputs;').fetchall()
        results = [tuple(row) for row in all_runs]
        return jsonify(results)

# Adding the api resources
api.add_resource(RunId, "/Run/<int:RunId>")
api.add_resource(Runs,"/")

# start
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT,debug=True)
