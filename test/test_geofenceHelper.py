from unittest import TestCase
from geofence.geofencehelper import GeofenceHelper
from shapely.geometry import Point

class TestGeofenceHelper(TestCase):
    def test_read_geofence_file(self):
        geofence = "../geofence/geofence.txt"
        geofence_to_coordinates = GeofenceHelper.read_geofence_file(geofence)
        expected = {'[raids]': [Point(48.13172583437477, 7.797374725341797), Point(48.11946535004539, 7.80252456665039),
                                Point(48.09975077428877, 7.84698486328125), Point(48.07039414422354, 7.859001159667968)],
                    '[raids2]': [Point(48.13172583437477, 7.797374725341797), Point(48.11946535004539, 7.80252456665039),
                                Point(48.09975077428877, 7.84698486328125), Point(48.07039414422354, 7.859001159667968)]
                    }
        self.assertDictEqual(expected, geofence_to_coordinates)

    def test_is_in_any_geofence(self):
        geofence = "../geofence/geofence.txt"
        helper = GeofenceHelper(geofencefile=geofence)
        points = [Point(48.094198, 7.842488), Point(48.095982, 7.842063), Point(48.097766, 7.848576)]
        self.assertEqual(True, helper.is_in_any_geofence(points[0]))
        self.assertEqual(True, helper.is_in_any_geofence(points[1]))
        self.assertEqual(False, helper.is_in_any_geofence(points[2]))

    def test_filter_coordinates(self):
        geofence = "../geofence/geofence.txt"
        helper = GeofenceHelper(geofencefile=geofence)
        points = [Point(48.094198, 7.842488), Point(48.095982, 7.842063), Point(48.097766, 7.848576)]
        inside, outside = helper.filter_coordinates(points)
        expected_inside = [Point(48.094198, 7.842488), Point(48.095982, 7.842063)]
        expected_outside = [Point(48.097766, 7.848576)]
        self.assertEqual(expected_inside, inside)
        self.assertEqual(expected_outside, outside)
