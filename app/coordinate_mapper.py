from datetime import datetime

from file_helper import FileHelper


class CoordinateMapper:

    def __init__(self):
        self.data = FileHelper.load_json_file('data/parkway_data.json')
        self.coordinates = FileHelper.load_json_file('data/static/milepost_coordinates.json')
        self.routes = FileHelper.load_json_file('data/static/routes.json')

    def map_coordinates(self):
        """takes the parkway table data and applies it to the stored route data to create geojson map data features"""
        features = [self.format_geojson_row(row) for row in self.routes]

        geojson = {
            'type': 'FeatureCollection',
            'metadata': {
                'last_update': self.data['last_update'],
                'last_request': datetime.now().strftime('%Y/%m/%d, %H:%M:%S'),
                'map_center': {'long': -82.55950927734376, 'lat': 35.570214567965984}
            },
            'features': features
        }
        FileHelper.save_json_file('data/map_data.geojson', geojson)

    def format_geojson_row(self, row):
        """creates a geojson feature containing the section information & 'route' to be displayed on the map"""

        data_row = self.data['road_statuses'].get(row['parkway_mileposts'], {})
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
                'status': data_row.get('status', 'ERR'),
                'notes': data_row.get('notes', ''),
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

        # if the mileposts are the same, then this is an access point and needs to be set up differently
        if row['starting_milepost'] == row['ending_milepost']:
            temp['properties']['name'] = start_name
            temp['properties']['description'] = start_description
            temp['geometry']['type'] = 'Point'
            temp['geometry']['coordinates'] = temp['geometry']['coordinates'][0]

        return temp
