# GeohashPy

**GeohashPy** is a comprehensive Python implementation of the Geohash algorithm.  
This package focuses on encoding and decoding geographic coordinates into a compact string format using the Geohash algorithm. The implementation is inspired by the algorithm described in [this blog post (Japanese)](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0).

---

## About This Project

This project was designed as both:
- **A sample implementation of Object-Oriented Programming (OOP)**, and
- **A learning resource to understand the Geohash algorithm**.

While performance and optimization are valuable, this library prioritizes a consistent design and the transparency of the algorithm for educational purposes. That said, we do aim to achieve reasonable performance improvements without sacrificing clarity.

#### Key Features:

- Provides a clean example demonstrating OOP principles clearly and intuitively.
- Emphasizes readability—making the Geohash algorithm easier to learn and understand.

---

## What is Geohash?

**Geohash** is a spatial data structure that encodes latitude and longitude (geographical coordinates) into a hierarchical and compact string representation. This structure efficiently represents the spatial proximity of locations using strings.

Key features of Geohash:
- **Recursive Division**: Geohash divides the Earth's surface into rectangular regions recursively along both latitude and longitude. This encoding allows for efficient storage and retrieval of geographic location data, although regions near the poles or the equator may appear slightly distorted.
- **Compact String Representation**: The precision of encoded coordinates depends on the length of the Geohash string. A 12-character Geohash, for instance, offers enough precision to represent locations with an accuracy of a few centimeters.
- **Database Efficiency**: Geohash encoding can improve database query speed by representing geospatial data as strings, rather than directly using latitude and longitude values.

### Precision Table

The following table shows the approximate resolution for Geohash strings of different lengths:

> **Note**: The resolution values are approximate and measured for locations near the equator. At higher latitudes, the resolution varies due to Earth's curvature.

| Length | Resolution (latitude x longitude) |
|--------|-----------------------------------|
| 1      | ±2500 km x ±5000 km              |
| 2      | ±630 km x ±1250 km               |
| 3      | ±78 km x ±156 km                 |
| 4      | ±20 km x ±39 km                  |
| 5      | ±2.4 km x ±4.9 km                |
| 6      | ±610 m x ±1.2 km                 |
| 7      | ±76 m x ±152 m                   |
| 8      | ±19 m x ±38 m                    |
| 9      | ±2.4 m x ±4.8 m                  |
| 10     | ±0.6 m x ±1.2 m                  |
| 11     | ±0.07 m x ±0.15 m                |
| 12     | ±0.018 m x ±0.038 m              |

By default, this library uses a precision level of 11. However, users can customize the precision to suit their specific requirements.

---

## Features

- Encode geographic coordinates into Geohash strings.
- Decode Geohash strings into latitude and longitude.
- Obtain neighboring Geohashes.
- Automatically normalize latitude and longitude values during operations.
- Validate and normalize coordinate and Geohash string inputs.
- Clear handling of coordinate normalization with practical examples.

---

## Requirements

To use this library, the following dependencies must be installed:

- **Required**: [`bitarray`](https://pypi.org/project/bitarray/)  
  Used for encoding and decoding processes within Geohash.

- **Optional**: [`matplotlib`](https://pypi.org/project/matplotlib/)  
  Only required for running examples like `./examples/geohash_precision_test.py`, which include graphical visualizations.

The library is compatible with Python 3.x (Python 3.7+ is recommended).

---

## Installation

1. **Install from PyPI:**

`GeohashPy` is published on PyPI, so it can be easily installed with the following command:

```sh
pip install geohash-py
```

The required `bitarray` dependency will be automatically installed.

2. **Clone the repository for development:**

If you’d like to explore the source code or use the library for development, you can clone the repository:

```sh
git clone https://github.com/layla777/geohash_py.git
cd geohash_py
```

3. **Install matplotlib for example code:**

To run example scripts that visualize precision testing, install `matplotlib`:

```sh
pip install matplotlib
```

---

## Usage

`Geohash` supports various methods for encoding, decoding, and normalizing geographic coordinates.

### Initialization

The `Geohash` class supports flexible initialization methods using either:
- Latitude and longitude, or
- A Geohash string.

#### Using Latitude and Longitude (`init_with_lat_lng` or `from_lat_lng`)

Both methods work identically and allow you to specify the precision (or "length") of the Geohash.

```python
from geohash_py import Geohash

# Using latitude and longitude
gh = Geohash.init_with_lat_lng(lat_lng=[37.7749, -122.4194], length=8)
print(gh.geohash)  # '9q8yyx4g'
```

#### Using Geohash String (`init_with_geohash` or `from_geohash`)

```python
# Using an existing Geohash string
gh = Geohash.init_with_geohash('9q8yy')
print(gh.geohash)  # '9q8yy'
```

**Note**: `length=` and `precision=` are interchangeable. Use one only.

---

### Encoding, Decoding & Neighbors

- **Encode Coordinates**: Updates an existing Geohash with new latitude and longitude values.

```python
gh.encode_with_lat_lng([34.0522, -118.2437], length=8)
print(gh.geohash)  # '9q5czqg8'
```

- **Decode Geohash to Intervals**: Retrieve the latitude and longitude range (bounds) represented by a Geohash string.

```python
lat_interval, lng_interval = gh.decode_to_interval()
print(lat_interval)  # (34.0517578125, 34.052734375)
print(lng_interval)  # (-118.244140625, -118.2431640625)
```

- **Decode Geohash to Center**: Retrieve latitude and longitude values corresponding to the center of the region.

```python
lat, lng = gh.decode()
print(lat, lng)  # Example: 34.0522, -118.2437
```

- **Neighbors**: Retrieve neighboring Geohash regions for spatial queries. The `order` parameter controls the range.

```python
# Get neighbors with order=1
neighbors = gh.neighbors(order=1)
print(neighbors)  # ['9q5cy', '9q5ct', ...]
```

---

### Technical Details

#### Latitude and Longitude Normalization

When working with latitude and longitude values, GeohashPy automatically normalizes out-of-range values as follows:

1. **Longitude Normalization**:
   - Longitude is adjusted to fit within the valid range of `-180° to +180°` using modular arithmetic.  
     Examples:
     - `190°` → `-170°`
     - `-200°` → `160°`

2. **Latitude Normalization**:
   - Latitude is folded into the valid range of `-90° to +90°`.  
     Examples:
     - `-95°` → `-85°`
     - `100°` → `80°`

This normalization ensures all geographic coordinates are valid representations on Earth. It also helps maintain high accuracy when working with edge cases (e.g., coordinates exceeding normal ranges).

---


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

The implementation is based on the Geohash algorithm detailed in [this blog post (Japanese)](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0).

We welcome contributions, suggestions, or feedback through pull requests or issue submissions.