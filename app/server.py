from flask import Flask, json, render_template
from flask_cors import CORS
from nc_parkway_scraper import NcParkwayScraper
from nc_coordinate_mapper import NcCoordinateMapper
from file_helper import FileHelper

api = Flask(__name__)
CORS(api)

@api.route('/sync_nc', methods=['GET'])
def sync_nc_parkway_data():
    # refresh road status
    ps = NcParkwayScraper()
    ps.load_table_data()

    # convert statuses into geojson
    cm = NcCoordinateMapper()
    cm.format_geojson()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@api.route('/nc_geojson', methods=['GET'])
def fetch_nc_geojson():
    # refresh road status
    data = FileHelper.load_json_file('data/nc_parkway_data.geojson')
    return json.dumps({'data':data}), 200, {'ContentType':'application/json'}

@api.route('/nc_map', methods=['GET'])
def display_nc_map():
    sync_nc_parkway_data()
    return render_template("nc_map.html")

if __name__ == '__main__':
    api.run()
