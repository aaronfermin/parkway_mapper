from data_syncer import DataSyncer
from coordinate_mapper import CoordinateMapper

syncer = DataSyncer()
syncer.sync(True)
cm = CoordinateMapper()
cm.map_coordinates()
