from data_syncer import DataSyncer
from coordinate_mapper import CoordinateMapper

# fetch road status and save to a file
syncer = DataSyncer()
syncer.sync()

print(syncer.road_statuses)

# load status file, format into geojson for the map to read
# cm = CoordinateMapper()
# cm.run()
