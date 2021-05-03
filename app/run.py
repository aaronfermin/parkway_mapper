from nc_parkway_scraper import NcParkwayScraper
from nc_coordinate_mapper import NcCoordinateMapper

# refresh road status
ps = NcParkwayScraper()
ps.load_table_data()

# convert statuses into geojson
cm = NcCoordinateMapper()
cm.format_geojson()

# print(pm.table_data)
