from datetime import datetime

import requests

from file_helper import FileHelper


class CoordinateMapper:

    def __init__(self):
        self.ors_base_url = 'https://api.openrouteservice.org'
        self.ors_api_key = '5b3ce3597851110001cf62486d7c9cafa72e4b4d848b4145884b2fe1'
        self.mapped_data = None
        self.load_nc_parkway_data()

    def map_coordinates(self):
        pass

    def load_nc_parkway_data(self):
        self.nc_parkway_data = FileHelper.load_json_file('data/nc_parkway_data.json')
        self.milepost_coordinates = FileHelper.load_json_file('data/nc_parkway_milepost_coordinates.json')['mileposts']
        self.data_with_routes = FileHelper.load_json_file('data/nc_parkway_data_with_routes.json')

    def format_geojson(self):
        features = list()
        for row in self.data_with_routes:
            feature = self.format_geojson_row(row)
            features.append(feature)
        geojson = {
            'type': 'FeatureCollection',
            'metadata': {
                'last_update': self.nc_parkway_data['last_update'],
                'last_request': datetime.now().strftime('%Y/%m/%d, %H:%M:%S'),
                'map_center': {'long': -82.55950927734376, 'lat': 35.570214567965984}
            },
            'features': features
        }
        FileHelper.save_json_file('data/nc_parkway_data.geojson', geojson)

    def format_geojson_row(self, row):
        # TODO: determine starting/ ending milepost here as it makes more sense than in the scraper
        mileposts = [milepost.strip() for milepost in cell[0].split('-')]
        parkway_row = self.find_parkway_row(row['parkway_mileposts'])
        start_name = row['starting_coordinate']['name']
        end_name = row['ending_coordinate']['name']
        start_description = row['starting_coordinate']['description'] or start_name
        end_description = row['ending_coordinate']['description'] or end_name
        temp = {
            'type': 'Feature',
            'properties': {
                'parkway_mileposts': row['parkway_mileposts'],
                'name': start_name + ' to ' + end_name,
                'description': start_description + ' to ' + end_description,
                'status': parkway_row['status'],
                'notes': parkway_row.get('notes'),
                'coordinates': {
                    'starting_coordinate': row['starting_coordinate'],
                    'ending_coordinate': row['ending_coordinate']
                },
                'mileposts': {
                    'starting_milepost': row['starting_milepost'],
                    'ending_milepost': row['ending_milepost']
                }
            },
            'geometry': {
                'coordinates': row['geojson']['features'][0]['geometry']['coordinates'],
                'type': 'LineString'
            }
        }
        if row['starting_milepost'] == row['ending_milepost']:
            temp['properties']['name'] = start_name
            temp['properties']['description'] = start_description
            temp['geometry']['type'] = 'Point'
            temp['geometry']['coordinates'] = temp['geometry']['coordinates'][0]
        return temp

    def find_parkway_row(self, mileposts):
        for row in self.nc_parkway_data['road_data']:
            if row['parkway_mileposts'] == mileposts:
                return row
        return None

    # Everything below this is only run once (unless I need to regen directions or regen coordinates)

    # This function
    # 1. assigns a lat & long coordinate to each milepost in nc_parkway_data
    # 2. calls openrouteservice.org to get a route for each table data row
    # 2a. saves all of the above merged data to nc_parkway_data_with_routes
    # 3. reformats the merged data into usable geojson
    def map_data_with_coords_and_geojson(self):
        self.assign_coordinates()
        self.assign_geojson_routes()
        self.format_geojson()

    def assign_coordinates(self):
        mapped_data = list()
        for row in self.nc_parkway_data['road_data']:
            if row['starting_milepost'] in self.milepost_coordinates:
                row['starting_coordinate'] = self.milepost_coordinates[row['starting_milepost']]
            if row['ending_milepost'] in self.milepost_coordinates:
                row['ending_coordinate'] = self.milepost_coordinates[row['ending_milepost']]
            if 'starting_coordinate' in row and 'ending_coordinate' in row:
                mapped_data.append(row)
        self.mapped_data = mapped_data

    def assign_geojson_routes(self):
        routes = list()
        for row in self.mapped_data:
            start = self.format_coordinate(row['starting_coordinate'])
            end = self.format_coordinate(row['ending_coordinate'])
            coordinates = {'start': start, 'end': end}
            response = self.fetch_geojson_route(coordinates)
            if response.status_code == 200:
                row['geojson'] = response.json()
            routes.append(row)
        FileHelper.save_json_file('data/nc_parkway_data_with_routes.json', routes)

    def fetch_geojson_route(self, coordinates):
        url = self.ors_base_url + '/v2/directions/driving-car'
        params = {'api_key': self.ors_api_key, 'start': coordinates['start'], 'end': coordinates['end']}
        return requests.get(url, params)

    def format_coordinate(self, coordinate):
        return coordinate['longitude'] + ',' + coordinate['latitude']

    # This function is just to give an empty template of unique mileposts
    # for the coordinate file since I have to visually assign each coordinate
    def generate_empty_json(self):
        data = {'mileposts': {}}
        mile_markers = set()
        for row in self.parkway_data['road_data']:
            mile_markers.add(row['starting_milepost'])
            mile_markers.add(row['ending_milepost'])
        for milepost in sorted(mile_markers):
            temp = {'name': '', 'description': '', 'longitude': '', 'latitude': ''}
            data['mileposts'][milepost] = temp
        FileHelper.save_json_file('data/nc_parkway_milepost_coordinates_empty.json', data)
