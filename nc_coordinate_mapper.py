    def assign_coordinates(self):
        coordinates = FileHelper.load_json_file('data/nc_parkway_milepost_coordinates.json')['mileposts']
        table_data = list()
        for row in self.table_data:
            temp = row
            start_coordinate, end_coordinate = None, None
            if row['starting_milepost'] in coordinates:
                temp['starting_coordinate'] = coordinates[row['starting_milepost']]
            if row['ending_milepost'] in coordinates:
                temp['ending_coordinate'] = coordinates[row['ending_milepost']]
            table_data.append(row)
        self.table_data = table_data
