from geohash import *

# テストケースの準備
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

# Geohash を計算して表示
for lat_lng, description in test_cases:
    print(f'{lat_lng}: {description}')
    for precision in range(1, 13):
        gh = Geohash.init_with_lat_lng(lat_lng, precision)
        print(f'  precision {precision}: {gh.get_geohash()}')
    print()
