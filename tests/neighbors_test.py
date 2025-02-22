import unittest

from geohash_py import Geohash


class TestGeohashNeighbors(unittest.TestCase):

    def test_neighbors_for_kyoto(self):
        """
        Unit test: Verify neighboring Geohashes for Kyoto
        (latitude: 35.0116, longitude: 135.7681).
        """
        # Kyoto's latitude and longitude
        lat, lng = 35.0116, 135.7681

        # Create a Geohash with precision length 9
        gh = Geohash.init_with_lat_lng([lat, lng], length=9)

        # Current Geohash for Kyoto
        current_geohash = gh.geohash
        print(f'Current geohash: {current_geohash}')

        # Get the neighbors using the method being tested
        neighbors = gh.neighbors(order=1)

        # Dynamically calculate the expected neighbors
        # The expected neighbors should be calculated based on the same logic as the neighbors method
        expected_neighbors_dynamic = []
        relative_positions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        interval_lat, interval_lng = gh.decode_to_interval()
        delta_lat = interval_lat[1] - interval_lat[0]
        delta_lng = interval_lng[1] - interval_lng[0]
        center_lat = (interval_lat[0] + interval_lat[1]) / 2
        center_lng = (interval_lng[0] + interval_lng[1]) / 2

        for i, j in relative_positions:
            adj_lat = Geohash._normalize_lat(center_lat + (i * delta_lat))
            adj_lng = Geohash._normalize_angle_180(center_lng + (j * delta_lng))
            expected_neighbors_dynamic.append(
                gh._encode(adj_lat, adj_lng, len(gh))
            )

        # Assert that the length of the neighbors is correct
        self.assertEqual(len(neighbors), 8, 'The number of neighbors should be 8.')

        # Assert that the neighbors match the dynamically calculated expected neighbors
        self.assertCountEqual(
            neighbors, expected_neighbors_dynamic,
            "Neighbors do not match the dynamically calculated expected neighbors."
        )
