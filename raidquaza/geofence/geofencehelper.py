from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from typing import List, Dict, Tuple
from globals.globals import LOGGER


class GeofenceHelper(object):
    def __init__(self, geofencefile):
        LOGGER.info("Initializing GeofenceHelper")
        self.geofences = dict()
        geofence_to_coordinates = GeofenceHelper.read_geofence_file(geofencefile)
        for geofence, coordinates in geofence_to_coordinates.items():
            self.geofences[geofence] = Polygon([(c.x, c.y) for c in coordinates])

    @staticmethod
    def read_geofence_file(geofence_file) -> Dict[str, List[Point]]:
        """
        Method which reads a geofence file and returns a dictionary with a mapping GEOFENCE -> COORDINATES
        :param geofence_file: A file containing a geofence.
        :return: Dict[str, List[Point]]
        """
        LOGGER.info("Reading geofence file: %s" % geofence_file)
        current_fence = 'unnamed'
        geofence_to_coordinates = dict()
        with open(geofence_file, 'r') as fence:
            for line in fence:
                if line.startswith('['):
                    current_fence = line.replace("\n", '')
                else:
                    line = line.replace("\n", '')
                    lat, lon = line.split(",")
                    if current_fence not in geofence_to_coordinates:
                        geofence_to_coordinates[current_fence] = []
                    geofence_to_coordinates[current_fence].append(Point(float(lat), float(lon)))
        return geofence_to_coordinates

    def is_in_any_geofence(self, coordinate: Point):
        for name, geofence in self.geofences.items():
            if coordinate.within(geofence):
                LOGGER.debug("coordinate: %s is in geofence: %s" % (coordinate, name))
                return True
        LOGGER.debug("coordinate: %s not in any geofence" % coordinate)
        return False

    def is_in_any_geofence(self, latitude: float, longitude: float):
        coordinate = Point(latitude, longitude)
        for name, geofence in self.geofences.items():
            if coordinate.within(geofence):
                LOGGER.debug("coordinate: %s is in geofence: %s" % (coordinate, name))
                return True
        LOGGER.debug("coordinate: %s not in any geofence" % coordinate)
        return False

    def filter_coordinates(self, coordinates: List[Point]) -> Tuple[List[Point], List[Point]]:
        inside = []
        outside = []
        for coord in coordinates:
            if self.is_in_any_geofence(coord):
                inside.append(coord)
            else:
                outside.append(coord)
        return inside, outside
