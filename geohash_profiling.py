import argparse
import cProfile
import io
import pstats

from geohash import Geohash


class GeohashProfiling:
    def __init__(self, repeat_count, lat_lng, geohash_str, output=None):
        """
        Function to profile and analyze the performance of Geohash class operations.

        Parameters:
            repeat_count (int): Number of repetitions for each test.
            lat_lng (list): Latitude and longitude to test encode/decode.
            geohash_str (str): Geohash string for initialization and operations.
            output (str): Optional file path to save the profiling results.
        """
        self.repeat_count = repeat_count
        self.lat_lng = lat_lng
        self.geohash_str = geohash_str
        self.output = output
        self.large_lat_lng = [3600.7749, -4320.4194]  # Large lat/lng values for normalization tests


    def test_operations(self):
        # 1. Initialization using latitude and longitude
        for _ in range(self.repeat_count // 10):  # Reduce workload
            _ = Geohash.init_with_lat_lng(self.lat_lng)

        # 2. Initialization using a geohash string
        for _ in range(self.repeat_count // 10):
            _ = Geohash.init_with_geohash(self.geohash_str)

        # 3. Test encode_with_lat_lng (including large values)
        geohash = Geohash.init_with_geohash(self.geohash_str)
        for _ in range(self.repeat_count // 5):
            geohash.encode_with_lat_lng(self.large_lat_lng)

        # 4. Test decode_to_interval
        for _ in range(self.repeat_count):
            geohash.decode_to_interval()

        # 5. Test decode
        for _ in range(self.repeat_count):
            geohash.decode()

        # 6. Test neighbors
        for _ in range(self.repeat_count // 10):
            _ = geohash.neighbors(order=2)


    def profile_operations(self):
        # Start profiling
        profiler = cProfile.Profile()
        profiler.enable()
        self.test_operations()
        profiler.disable()

        # Format and display profiling results
        result = io.StringIO()
        stats = pstats.Stats(profiler, stream=result)
        stats.strip_dirs()
        stats.sort_stats('cumulative')
        stats.print_stats(20)
        if self.output:
            with open(self.output, 'w') as file:
                file.write(result.getvalue())
        else:
            print(result.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Profile and analyze the performance of Geohash operations."
    )
    parser.add_argument(
        '--repeat_count',
        type=int,
        default=10000,
        help='Number of repetitions for testing all operations (default: 10000).',
    )
    parser.add_argument(
        '--lat_lng',
        type=float,
        nargs=2,
        default=[37.7749, -122.4194],
        help='Latitude and longitude as a pair (default: [37.7749, -122.4194]).',
    )
    parser.add_argument(
        '--geohash_str',
        type=str,
        default='9q8yyzjfwqr',
        help='Geohash string for initialization (default: "9q8yyzjfwqr").',
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Optional file to save profiling results (default: stdout).',
    )
    args = parser.parse_args()
    profiler = GeohashProfiling(
        repeat_count=args.repeat_count,
        lat_lng=args.lat_lng,
        geohash_str=args.geohash_str,
        output=args.output,
    )
    profiler.profile_operations()
