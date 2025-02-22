"""
geohash_profiling.py

This script is designed to profile and analyze the performance of the Geohash class operations.
By running this script, you can pinpoint potential bottlenecks in the Geohash implementation
through various encode, decode, and neighbor-related operations.

How to use:
1. Ensure the required Geohash implementation is accessible and this script has the necessary imports.
2. Run the script in the terminal with customizable arguments, for example:
   python geohash_profiling.py --data_size 5000 --output profile_results.txt

Arguments:
- `--data_size`: Number of data size for testing (default: 10000). Affects profiling detail.
- `--output`: File path to save the profiling results. If not provided, results will
              be displayed in the terminal (default: None).

What the script does:
1. Initializes the Geohash class with given latitude/longitude or geohash strings.
2. Tests various Geohash class methods such as encode, decode, and neighbor calculation.
3. Profiles the performance of these operations with `cProfile` and generates a
   detailed analysis of the most time-consuming methods.

Expected result:
- A profiling summary showing the top methods consuming the most runtime with cumulative and per-call stats.
- If specified, a detailed profile written to the output file.

This script is especially useful for:
- Developers optimizing Geohash performance.
- Learning the runtime costs of various Geohash operations under different conditions.
- Debugging bottlenecks in large-scale location-based systems.
"""
import argparse
import cProfile
import io
import json
import pstats
import random
import time

from geohash_py import Geohash

LAT_LNG_MAX_RANGE = 300


class GeohashProfiling:
    """
    Profile and analyze the performance of Geohash class operations.

    Attributes:
        data_size (int): Number of randomly generated latitude and longitude pairs to test.
        output (str): Optional file path where profiling results will be saved.
        lat_lng_pairs (list): Randomly generated (latitude, longitude) pairs. Includes out-of-range values.
        geohashes (list): Geohash objects created from the lat/lng pairs.
        geohash_str_list (list): Corresponding geohash strings of the created Geohash objects.

    Note:
        The lat_lng_pairs include out-of-range values purposely.
        This measures the performance of normalization processes in the Geohash implementation.
    """

    def __init__(self, data_size, output=None):
        """Initialize GeohashProfiling with the test data size and optional output file."""
        self.data_size = data_size
        self.output = output

        # Generate random latitude/longitude pairs. Out-of-range values are included to test normalization performance.
        self.lat_lng_pairs = [
            [self.random_lat_lng_generator(), self.random_lat_lng_generator()]
            for _ in range(data_size)
        ]

        # Predefine Geohash objects and strings for other test cases.
        self.geohashes = [Geohash.init_with_lat_lng(lat_lng) for lat_lng in self.lat_lng_pairs]
        self.geohash_str_list = [geohash.geohash for geohash in self.geohashes]

    @staticmethod
    def random_lat_lng_generator():
        """
        Generate a random latitude/longitude value.

        Note:
            The generated value can exceed the valid geographic ranges:
            - Latitude: [-90, 90]
            - Longitude: [-180, 180]
            This is intentional to test the Geohash class's normalization performance.
        """
        return (random.random() * 2 - 1) * LAT_LNG_MAX_RANGE

    def test_operations(self):
        """
            Run various Geohash methods repeatedly to simulate a realistic workload.

            This function measures the execution time of:
            - Geohash initialization with latitude/longitude.
            - Geohash initialization with a geohash string.
            - Decoding a geohash to intervals.
            - Decoding a geohash to coordinates.
            - Calculating neighbors for geohashes.

            Returns:
                dict: Execution times for each operation in seconds.
            """
        operation_times = {}

        # 1. Initialize Geohash using latitude and longitude
        # Measure the time it takes to normalize and encode random lat/lng pairs.
        start = time.time()
        for lat_lng in self.lat_lng_pairs:  # Reduced workload
            _ = Geohash.init_with_lat_lng(lat_lng)
        operation_times['init_with_lat_lng'] = time.time() - start

        # 2. Initialize Geohash using a string
        # Decode geohash strings back to objects
        start = time.time()
        for geohash_str in self.geohash_str_list:
            _ = Geohash.init_with_geohash(geohash_str)
        operation_times['init_with_geohash'] = time.time() - start

        # 3. Decode to intervals
        # Test the accuracy and speed of the decode_to_interval method
        start = time.time()
        for geohash in self.geohashes:
            geohash.decode_to_interval()
        operation_times['decode_to_interval'] = time.time() - start

        # 4. Decode to coordinates
        # Decode Geohash objects into latitude/longitude pairs.
        start = time.time()
        for geohash in self.geohashes:
            geohash.decode()
        operation_times['decode'] = time.time() - start

        # 5. Calculate neighbors
        # Measure the performance of finding first-order neighbors of the geohash.
        start = time.time()
        for geohash in self.geohashes:
            _ = geohash.neighbors(order=1)
        operation_times['neighbors'] = time.time() - start

        return operation_times

    def profile_operations(self):
        """
        Profile the Geohash operations using cProfile.

        This function generates a detailed performance analysis of the Geohash
        operations and prints/saves the profiling results.

        Summary:
            - Initializes a cProfile profiler.
            - Runs the defined Geohash operations and measures elapsed time.
            - Outputs profiling results to a file or displays them in the terminal.

        Creates:
            JSON profiling report containing:
            - Total elapsed time for all operations.
            - Breakdown of operation times.
            - Statistical summary (cumulative timings for key function calls).
        """
        profiler = cProfile.Profile()
        start_time = time.time()

        # Start the profiler and run all Geohash operations
        profiler.enable()
        operation_times = self.test_operations()
        profiler.disable()
        elapsed_time = time.time() - start_time

        # Generate profiling report as a statistical summary
        result = io.StringIO()
        stats = pstats.Stats(profiler, stream=result)
        stats.strip_dirs()  # Remove unnecessary directory prefixes
        stats.sort_stats('cumulative')  # Sort by cumulative execution time
        stats.print_stats(20)  # Print the top 20 slowest functions

        # Prepare profiling result in JSON
        profiling_data = {
            'elapsed_time': elapsed_time,
            'operation_times': operation_times,
            'statistical_summary': result.getvalue(),
        }

        # Display profiling results or save to an output file
        if self.output:
            try:
                # Save profiling data to a specified file as JSON
                with open(self.output, 'w') as f:
                    f.write(json.dumps(profiling_data, indent=4))
                print(f'Profiling results successfully saved to {self.output}')
            except IOError as e:
                print(f'Failed to save profiling results to {self.output}: {e}')
        else:
            # Print profiling results to the terminal
            print(result.getvalue())
            print(f'\nTotal elapsed time: {elapsed_time:.4f} seconds')

        # Provide a time breakdown for each individual operation
        print('\n=== Time Breakdown ===')
        for op, t in operation_times.items():
            print(f'{op}: {t:.4f} seconds')


def display_cache_info():
    """
    Display cache hit/miss information for key Geohash methods.

    This function retrieves and prints the cache statistics (if available)
    from methods decorated with @lru_cache.
    """
    print('===== Cache Info =====')
    try:
        # Print cache usage for key utility methods
        print ('Neighbors', Geohash.neighbors.cache_info())
        print('Generate Relative Positions', Geohash.generate_relative_positions.cache_info())
        print('Geohash to Bits:', Geohash._geohash_to_bits.cache_info())
    except AttributeError:
        # Notify if cache information is unavailable
        print('Cache info is not available. Ensure @lru_cache is applied.')
    print('======================')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Profile and analyze Geohash operations.')
    parser.add_argument(
        '--data_size',
        type=int,
        default=10000,
        help='Number of data size for testing operations (default: 10000).',
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Optional output file to save profiling results (default: stdout).',
    )
    args = parser.parse_args()

    # Run profiling
    profiler = GeohashProfiling(
        data_size=args.data_size,
        output=args.output,
    )
    profiler.profile_operations()

    # Display cache statistics
    display_cache_info()
