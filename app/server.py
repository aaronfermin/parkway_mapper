from flask import Flask, json, render_template
from flask_cors import CORS
from data_syncer import DataSyncer
from coordinate_mapper import CoordinateMapper
from file_helper import FileHelper

api = Flask(__name__)
CORS(api)


@api.route('/sync_data', methods=['GET'])
def sync_data():
    # force fetch road status and save to a file
    syncer = DataSyncer()
    syncer.sync(force_update=True)

    # load status file, format into geojson for the map to read
    mapper = CoordinateMapper()
    mapper.map_coordinates()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@api.route('/fetch_geojson', methods=['GET'])
def fetch_geojson():
    data = FileHelper.load_json_file('data/nc_parkway_data.geojson')
    return json.dumps({'data': data}), 200, {'ContentType': 'application/json'}


@api.route('/', methods=['GET'])
def display_map():
    try:
        sync_data()
    except Exception as e:
        json.dumps({'error': str(e)}), 500, {'ContentType': 'application/json'}
        raise
    return render_template('nc_map.html')


if __name__ == '__main__':
    api.run()
