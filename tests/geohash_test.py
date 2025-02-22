import unittest

from .geohash_profiling import GeohashProfiling
from geohash_py import Geohash


class TestGeohash(unittest.TestCase):
    # ------------ API Usage and Compatibility Tests ------------ #
    def test_init_with_lat_lng_and_from_lat_lng(self):
        """Test that `init_with_lat_lng` and `from_lat_lng` produce the same result."""
        lat_lng = [37.7749, -122.4194]
        geohash1 = Geohash.init_with_lat_lng(lat_lng, precision=8)
        geohash2 = Geohash.from_lat_lng(lat_lng, precision=8)
        self.assertEqual(geohash1.geohash, geohash2.geohash)

    def test_init_with_geohash_and_from_geohash(self):
        """Test that `init_with_geohash` and `from_geohash` produce the same result."""
        geohash_str = "9q8yyzj"
        geohash1 = Geohash.init_with_geohash(geohash_str)
        geohash2 = Geohash.from_geohash(geohash_str)
        self.assertEqual(geohash1.geohash, geohash2.geohash)

    # ------------ Precision and Length Parameter Tests ------------ #
    def test_length_and_precision_exclusivity(self):
        """Test that `length` and `precision` cannot be both specified."""
        with self.assertRaises(ValueError):
            Geohash.from_lat_lng([37.7749, -122.4194], length=7, precision=8)

    def test_precision_method(self):
        """Test the precision() method for retrieving precision length."""
        geohash = Geohash.from_lat_lng([40.7128, -74.0060], precision=5)
        self.assertEqual(geohash.precision, 5)

    # ------------ Known Geohash Results Tests ------------ #
    def test_known_geohash_results(self):
        """Test known geohash results at different precision levels."""
        test_cases = [
            ([37.7749, -122.4194], "9q8yyk", 6),  # San Francisco
            ([40.7128, -74.0060], "dr5regw", 7),  # New York City
            ([90.0, 180.0], "zzzzzz", 6),  # North-East Max
        ]
        for lat_lng, expected_geohash, precision in test_cases:
            with self.subTest(lat_lng=lat_lng, precision=precision):
                geohash = Geohash.from_lat_lng(lat_lng, precision=precision)
                self.assertEqual(geohash.geohash, expected_geohash)

    # ------------ Neighbors Tests ------------ #
    def test_neighbors_various_orders(self):
        """Test neighbors at different orders."""
        geohash = Geohash.from_geohash("9q8yyzjfwqr")
        for order in range(1, 4):  # Test orders 1 to 3
            with self.subTest(order=order):
                neighbors = geohash.neighbors(order=order)
                self.assertEqual(len(neighbors), (order * 2 + 1) ** 2 - 1)
                for n in neighbors:
                    self.assertIsInstance(n, str)
                self.assertEqual(len(n), len(geohash.geohash))

    # ------------ Edge Cases and Outlier Handling ------------ #
    def test_outlier_coordinates_normalization(self):
        """Test normalization of outlier coordinates."""
        outlier_test_cases = [
            ([95.0, 100.0], 'Latitude exceeds 90 (95).'),
            ([-95.0, 100.0], 'Latitude below -90 (-95).'),
            ([45.0, 190.0], 'Longitude exceeds 180 (190).'),
            ([45.0, -200.0], 'Longitude below -180 (-200).'),
            ([100.0, 200.0], 'Both latitude and longitude are out of range (lat: 100, lon: 200).'),
            ([-100.0, -200.0], 'Both latitude and longitude are out of range (lat: -100, lon: -200).'),
        ]

        # Execute the tests
        for lat_lng, description in outlier_test_cases:
            with self.subTest(lat_lng=lat_lng):
                print(f'Testing normalization for {lat_lng}: {description}')
                for precision in range(1, 13):
                    try:
                        geohash = Geohash.init_with_lat_lng(lat_lng, precision)
                        print(f'  precision {precision}: {geohash.geohash}')
                    except Exception as e:
                        self.fail(f"Normalization failed for {lat_lng} at precision {precision}: {e}")

    # ------------ Deprecated Functionality Tests ------------ #
    def test_get_geohash_deprecation_warning(self):
        """Test that calling `get_geohash()` raises a DeprecationWarning."""
        geohash_str = "9q8yyzjfwqr"
        geohash = Geohash.init_with_geohash(geohash_str)
        with self.assertWarns(DeprecationWarning) as warning:
            result = geohash.get_geohash()
        self.assertEqual(result, geohash_str)
        self.assertIn("get_geohash() is deprecated and will be removed in a future version.",
                      str(warning.warning))

    def test_set_geohash_deprecation_warning(self):
        """Test that calling `set_geohash()` raises a DeprecationWarning."""
        geohash = Geohash.init_with_geohash("9q8yyzjfwqr")
        new_geohash = "s0000000000"
        with self.assertWarns(DeprecationWarning) as warning:
            geohash.set_geohash(new_geohash)
        self.assertEqual(geohash.geohash, new_geohash)
        self.assertIn("set_geohash() is deprecated and will be removed in a future version.",
                      str(warning.warning))

    # ------------ Profiling Functionality Tests ------------ #
    def test_profiling(self):
        """Test profiling of Geohash operations."""
        profiler = GeohashProfiling(data_size=100)
        try:
            profiler.profile_operations()
        except Exception as e:
            self.fail(f"GeohashProfiling.profile_operations() raised an exception: {e}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
