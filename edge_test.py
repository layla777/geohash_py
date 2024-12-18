# This script demonstrates geohashing by processing theoretical edge cases of latitude and longitude
# coordinates, representing extreme boundaries of Earth's geographical locations. It generates geohashes
# with various precision levels and outputs the results in a structured format.

# Script Usage:
# 1. Define test cases in the `test_cases` list, where each item contains a pair of [latitude, longitude]
#    and a description.
# 2. The script computes geohashes for each coordinate over precision levels from 1 to 12.
# 3. For each precision level, the geohash value is displayed along with its precision.

from geohash import Geohash

# Preparing test cases
test_cases = [
    ([-90.0, -180.0], 'South Pole with Min Longitude (West)'),
    ([-90.0, 0.0], 'South Pole'),
    ([-90.0, 180.0], 'South Pole with Max Longitude (East)'),
    ([0.0, -180.0], 'Equator and Min Longitude (West)'),
    ([0.0, 0.0], 'Equator and Prime Meridian'),
    ([0.0, 180.0], 'Equator and Max Longitude (East)'),
    ([90.0, -180.0], 'North Pole with Min Longitude (West)'),
    ([90.0, 0.0], 'North Pole'),
    ([90.0, 180.0], 'North Pole with Max Longitude (East)'),
]

# Calculate and display Geohash
for lat_lng, description in test_cases:
    print(f'{lat_lng}: {description}')
    for precision in range(1, 13):
        gh = Geohash.init_with_lat_lng(lat_lng, precision)
        print(f'  precision {precision}: {gh.get_geohash()}')
    print()
