#!/usr/bin/python
import MySQLdb
from flask import request, jsonify
import flask
from flask_googlemaps import GoogleMaps
from flask_googlemaps import get_address, get_coordinates

#from flask_googlemaps import GoogleMaps
API_KEY = 'AIzaSyAHu5-l3lWDBSpmMiYC_tsBQR5taO1GCvE'
app = flask.Flask(__name__)
app.config["DEBUG"] = True
#GoogleMaps(app, key="AIzaSyAHu5-l3lWDBSpmMiYC_tsBQR5taO1GCvE")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return '''Prototype API for gathering info about SFO FOOD TRUCKS'''


@app.route('/api/v1/foodtrucks/all', methods=['GET'])
def api_all():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="foodTrucks")        # name of the data base
    cur = db.cursor()
    cur.execute('SELECT DISTINCT Applicant, Address FROM Mobile_Food_Facility_Permit;')
    row_headers=[x[0] for x in cur.description]
    all_foodtrucks = cur.fetchall()
    json_data=[]
    for result in all_foodtrucks:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

@app.errorhandler(404)
def page_not_found(e):
    return "404. The resource could not be found.", 404

@app.route('/api/v1/foodtrucks', methods=['GET'])
def api_filter():
    query_parameters = request.args

    Applicant = query_parameters.get('Applicant')
    FacilityType = query_parameters.get('FacilityType')
    Address = query_parameters.get('Address')
    FoodItems = query_parameters.get('FoodItems')

    query = "SELECT Applicant,Address,FacilityType,FoodItems FROM Mobile_Food_Facility_Permit WHERE"
    to_filter = []

    if Applicant:
        query += ' Applicant=(%s) AND'
        to_filter.append(Applicant)
    if FacilityType:
        query += ' FacilityType=(%s) AND'
        to_filter.append(FacilityType)
    if Address:
        query += ' Address=(%s) AND'
        to_filter.append(Address)
    if FoodItems:
        query += ' FoodItems Like %s AND'
        to_filter.append(FoodItems)
    if not (Applicant or FacilityType or Address or FoodItems):
        return page_not_found(404)

    query = query[:-4] + ';'
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="foodTrucks")        # name of the data base
    cur = db.cursor()
    cur.execute(query, to_filter)
    result = cur.fetchall()
    return jsonify(result)

# @app.route('/api/v1/foodtrucks/address', methods=['GET'])
# def api_address():
#     Latitude = query_parameters.get('Latitude')
#     Longitude = query_parameters.get('Longitude')
#     Applicant = query_parameters.get('Applicant')
#
#     query = "SELECT Latitude, Longitude FROM Mobile_Food_Facility_Permit WHERE Applicant=(%s)"
#     to_filter = []
#
#     print(get_address(API_KEY,22.4761596,88.4149326))
#     return '''Prototype API for gathering info '''

# @app.route("/api/v1/foodtrucks/address")
# def mapview():
#     # creating a map in the view
#     mymap = Map(
#         identifier="view-side",
#         lat=37.4419,
#         lng=-122.1419,
#         markers=[(37.4419, -122.1419)]
#     )
#
app.run()
