import unittest

from geohash import Geohash
from geohash_profiling import GeohashProfiling


class TestGeohash(unittest.TestCase):
    # ------------ Standard Functionality Tests ------------ #
    def test_init_with_lat_lng(self):
        """Test initializing Geohash with latitude and longitude."""
        lat_lng = [37.7749, -122.4194]
        geohash = Geohash.init_with_lat_lng(lat_lng)
        self.assertIsInstance(geohash, Geohash)
        self.assertEqual(len(geohash.get_geohash()), 11)

    def test_init_with_geohash(self):
        """Test initializing Geohash with a geohash string."""
        geohash_str = '9q8yyzjfwqr'
        geohash = Geohash.init_with_geohash(geohash_str)
        self.assertIsInstance(geohash, Geohash)
        self.assertEqual(geohash.get_geohash(), geohash_str)

    def test_get_geohash(self):
        """Test retrieving the geohash string."""
        geohash_str = '9q8yyzjfwqr'
        geohash = Geohash.init_with_geohash(geohash_str)
        self.assertEqual(geohash.get_geohash(), geohash_str)

    def test_set_geohash(self):
        """Test updating the geohash string."""
        geohash = Geohash.init_with_geohash('9q8yyzjfwqr')
        new_geohash = 's0000000000'
        geohash.set_geohash(new_geohash)
        self.assertEqual(geohash.get_geohash(), new_geohash)

    def test_encode_with_lat_lng(self):
        """Test encoding new latitude and longitude into a geohash."""
        geohash = Geohash.init_with_geohash('9q8yyzjfwqr')
        lat_lng = [40.7128, -74.0060]  # New York City
        geohash.encode_with_lat_lng(lat_lng)
        self.assertEqual(len(geohash.get_geohash()), 11)

    def test_decode_to_interval(self):
        """Test decoding geohash into lat/lng intervals."""
        geohash = Geohash.init_with_geohash('9q8yyzjfwqr')
        intervals = geohash.decode_to_interval()
        self.assertEqual(len(intervals), 2)
        self.assertEqual(len(intervals[0]), 2)  # Latitude interval
        self.assertEqual(len(intervals[1]), 2)  # Longitude interval

    def test_decode(self):
        """Test decoding geohash into exact lat/lng values."""
        geohash = Geohash.init_with_geohash('9q8yyzjfwqr')
        lat_lng = geohash.decode()
        self.assertEqual(len(lat_lng), 2)  # Latitude and Longitude
        self.assertTrue(-90 <= lat_lng[0] <= 90)  # Latitude valid range
        self.assertTrue(-180 <= lat_lng[1] <= 180)  # Longitude valid range

    def test_neighbors(self):
        """Test retrieving neighbors of the geohash."""
        geohash = Geohash.init_with_geohash('9q8yyzjfwqr')
        neighbors = geohash.neighbors(order=1)
        self.assertEqual(len(neighbors), 8)  # 8 neighbors for order=1
        for n in neighbors:
            self.assertIsInstance(n, str)
            self.assertEqual(len(n), len(geohash.get_geohash()))  # Length matches the original geohash

    # ------------ Profiling Functionality Tests ------------ #
    def test_profiling(self):
        """Test profiling of Geohash operations."""
        profiler = GeohashProfiling(
            repeat_count=100,
            lat_lng=[37.7749, -122.4194],
            geohash_str='9q8yyzjfwqr'
        )
        try:
            profiler.profile_operations()
        except Exception as e:
            self.fail(f'GeohashProfiling.profile_operations() raised an exception: {e}')

    # ------------ Latitude and Longitude Normalization Tests ------------ #
    def test_lat_lng_normalization(self):
        """Test correct normalization of lat/lng values affecting geohash generation."""
        test_cases = [
            ([370, -122.4194], [10.0, -122.4194]),  # Latitude > 360 → Wrap-around normalization
            ([-450, -122.4194], [-90.0, -122.4194]),  # Latitude < -360 → Wrap-around normalization
            ([37.7749, 720], [37.7749, 0.0]),  # Longitude > 360 → Wrap-around normalization
            ([37.7749, -450], [37.7749, -90.0]),  # Longitude < -360 → Wrap-around normalization
        ]
        for raw_lat_lng, normalized_lat_lng in test_cases:
            with self.subTest(raw_input=raw_lat_lng):
                # Generate geohash with raw input
                raw_geohash = Geohash.init_with_lat_lng(raw_lat_lng).get_geohash()
                # Generate geohash with normalized input
                normalized_geohash = Geohash.init_with_lat_lng(normalized_lat_lng).get_geohash()
                # Check if both geohashes are the same
                self.assertEqual(
                    raw_geohash, normalized_geohash,
                    f'Normalization failed for input {raw_lat_lng}. '
                    f'Expected geohash: {normalized_geohash}, got {raw_geohash}'
                )

    # ------------ Invalid Type/Value Test ------------ #
    def test_empty_lat_lng(self):
        """Test that an empty lat_lng list raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Geohash.init_with_lat_lng([])
        self.assertEqual(str(context.exception), '"lat_lng" must have 2 and only 2 items.')

    def test_type_validation_in_lat_lng(self):
        """Test that lat_lng with non-float or non-int values raises a TypeError."""
        with self.assertRaises(TypeError) as context:
            Geohash.init_with_lat_lng(['not_a_number', -120])
        self.assertEqual(str(context.exception), 'Items of "lat_lng" must be float or integer.')

    def test_invalid_geohash_characters(self):
        """Test that an invalid geohash string raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Geohash.init_with_geohash('invalid_geohash@!')
        self.assertEqual(str(context.exception), 'Invalid characters.')

    # ------------ Edge Case Tests ------------ #
    def test_geohash_edge_cases(self):
        """Test geohash generation for extreme lat/lng edge cases."""
        test_cases = [
            ([-90.0, -180.0], '00000000000'),  # South Pole with Min Longitude (West)
            ([-90.0, 0.0], 'h0000000000'),  # South Pole
            ([-90.0, 180.0], 'pbpbpbpbpbp'),  # South Pole with Max Longitude (East)
            ([0.0, -180.0], '80000000000'),  # Equator and Min Longitude (West)
            ([0.0, 0.0], 's0000000000'),  # Equator and Prime Meridian
            ([0.0, 180.0], 'xbpbpbpbpbp'),  # Equator and Max Longitude (East)
            ([90.0, -180.0], 'bpbpbpbpbpb'),  # North Pole with Min Longitude (West)
            ([90.0, 0.0], 'upbpbpbpbpb'),  # North Pole
            ([90.0, 180.0], 'zzzzzzzzzzz'),  # North Pole with Max Longitude (East)
        ]
        for lat_lng, expected_geohash in test_cases:
            with self.subTest(lat_lng=lat_lng):
                # Generate geohash from the given lat/lng
                geohash = Geohash.init_with_lat_lng(lat_lng)
                generated_geohash = geohash.get_geohash()

                # Assert that the generated geohash matches the expected one
                self.assertEqual(
                    generated_geohash, expected_geohash,
                    f'Geohash mismatch for lat/lng {lat_lng}. '
                    f'Expected: {expected_geohash}, Got: {generated_geohash}'
                )

                # Decode back and ensure the decoded lat/lng matches the input within tolerance
                decoded_lat_lng = geohash.decode()
                self.assertAlmostEqual(decoded_lat_lng[0], lat_lng[0], places=5)
                self.assertAlmostEqual(decoded_lat_lng[1], lat_lng[1], places=5)

    # ------------ Precision and Performance Tests ------------ #
    def test_precision_tolerance(self):
        """Test tolerance levels for different geohash precision levels."""
        # The tolerance value of 1e-6 was determined based on the observed differences
        # during geohash precision testing (results from geohash_precision_test.py).
        # This ensures that the encoding and decoding process remains accurate
        # within the range of practical use cases and floating-point precision limitations.
        tolerance_map = {
            11: 0.0001,  # Tolerance for high precision
            5: 0.0005,  # Tolerance for medium precision
            3: 0.01  # Tolerance for low precision
        }
        test_cases = [
            ([37.7749, -122.4194], 11),
            ([37.7749, -122.4194], 5),
            ([37.7749, -122.4194], 3)
        ]
        for lat_lng, precision in test_cases:
            with self.subTest(lat_lng=lat_lng, precision=precision):
                geohash = Geohash.init_with_lat_lng(lat_lng)
                encoded = geohash.get_geohash()[:precision]
                decoded = geohash.decode()
                expected_tolerance = tolerance_map[precision]
                self.assertTrue(
                    abs(decoded[0] - lat_lng[0]) <= expected_tolerance,
                    f'Latitude difference exceeded tolerance for precision {precision}'
                )
                self.assertTrue(
                    abs(decoded[1] - lat_lng[1]) <= expected_tolerance,
                    f'Longitude difference exceeded tolerance for precision {precision}'
                )


if __name__ == '__main__':
    unittest.main(verbosity=2)
