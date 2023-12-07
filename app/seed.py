# This is code that I wrote to help generate files. Keeping it in case I have to do it all over again
# It's missing imports and shit, but I don't expect to run it anytime soon. Just don't wanna have to search git history

# self.ors_base_url = 'https://api.openrouteservice.org'
# self.ors_api_key = os.getenv('ORS_API_KEY')

def map_data_with_coords_and_geojson(self):
    # This function
    # 1. assigns a lat & long coordinate to each milepost in nc_parkway_data
    # 2. calls openrouteservice.org to get a route for each table data row
    # 2a. saves all of the above merged data to nc_parkway_routes
    # 3. reformats the merged data into usable geojson
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
    FileHelper.save_json_file('data/routes.json', routes)


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
