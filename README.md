
# GeohashPy

A Python library for encoding and decoding geographic coordinates using the Geohash algorithm. This implementation closely follows the principles outlined in [this blog post](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0), providing clarity and functionality for practical geohashing needs.

## About This Project
This project serves both as an **educational resource for Object-Oriented Programming (OOP)** and a **robust implementation of the Geohash algorithm**. It focuses on clear design principles and precise algorithm implementation to ensure reliability and transparency.

#### Key Features:
- Demonstrates clear and practical OOP design patterns.
- Offers an easy-to-understand and versatile Geohash algorithm implementation for learners and professionals alike.

## What is Geohash?

Geohash is an algorithm and spatial data structure that encodes geographic coordinates into a compact, human-readable format. Its key characteristics include:

- **Recursive Subdivision**: The Earth's surface is progressively divided into nested rectangular regions, with each subdivision offering higher precision.
- **Rectangular Regions**: Each Geohash string maps to a rectangular area on the globe. Due to the algorithm's design, some regions may be irregular in shape.
- **Compact Representation**: Geohash strings are concise, and their length determines the level of precision.

### Example of Irregular Rectangles

Consider a Geohash string that represents a region spanning the equator. The division of regions sometimes results in rectangles that vary significantly in size as you move towards the poles, highlighting the irregularity.

### Precision Table

The table below shows the approximated resolutions for Geohash strings of different lengths:
> **Note**: The resolutions listed in the table represent approximations near the equator. As latitude increases and approaches the poles, the longitudinal resolution (east-west direction) becomes finer due to the curvature of the Earth.

| Length | Resolution (Lat x Lng)       |
|--------|-----------------------------|
| 1      | ±2500 km x ±5000 km         |
| 2      | ±630 km x ±1250 km          |
| 3      | ±78 km x ±156 km            |
| 4      | ±20 km x ±39 km             |
| 5      | ±2.4 km x ±4.9 km           |
| 6      | ±610 m x ±1.2 km            |
| 7      | ±76 m x ±152 m              |
| 8      | ±19 m x ±38 m               |
| 9      | ±2.4 m x ±4.8 m             |
| 10     | ±0.6 m x ±1.2 m             |
| 11     | ±0.07 m x ±0.15 m           |

The library defaults to a precision of 11, but users can specify custom lengths depending on their requirements.

### Library Design Philosophy

The library accepts all valid Geohash strings, including those representing irregular rectangles. The irregularity is a natural consequence of the algorithm and is key to its flexibility in representing geographic space.

## Features

- Encode geographical coordinates into a geohash string
- Decode a geohash string back to latitude and longitude coordinates
- Retrieve neighboring geohashes for a given geohash
- Latitude and longitude are normalized during processing
- Input validation for coordinates and geohash strings
- Latitude and longitude normalization
- Explicit examples showing how latitude and longitude are normalized during processing

## Installation

Clone the repository to your local machine:

```sh
git clone https://github.com/layla777/geohash_py.git
cd geohash_py
```

This library is implemented in pure Python and does not require any additional dependencies.

## How to Use
Here's how you can use the `Geohash` class to encode, decode, and normalize geohashes, initialize them with specific values, and understand latitude and longitude normalization.

### Initializing a Geohash Object

The `Geohash` object should be initialized using one of the recommended methods:

#### **Recommended**: Using Latitude and Longitude (`init_with_lat_lng`)

```python
from geohash import Geohash

# Initialize with latitude and longitude
lat_lng = [37.7749, -122.4194]  # San Francisco, CA
length = 8
gh = Geohash.init_with_lat_lng(lat_lng=lat_lng, length=length)
print('Generated geohash:', gh.get_geohash())
```

#### **Recommended**: Using a Geohash String (`init_with_geohash`)

```python
# Initialize with a geohash string
geohash_str = '9q8yy'
gh = Geohash.init_with_geohash(geohash_str)
print('Geohash:', gh.get_geohash())
```

### Encoding Coordinates

You can encode new coordinates into the existing geohash object:

```python
# Encode new coordinates
new_lat_lng = [34.0522, -118.2437]  # Los Angeles, CA
gh.encode_with_lat_lng(new_lat_lng, length)
print('New geohash:', gh.get_geohash())
```

### Decoding a Geohash

You can decode a geohash string back into latitude and longitude:

```python
# Decode geohash
lat_lng = gh.decode()
print('Decoded coordinates:', lat_lng)
```

### Normalizing Latitude and Longitude

When working with geographic coordinates, latitude and longitude are automatically adjusted to their valid ranges during geohash processing. For details, refer to the [Technical Details](#technical-details) section.

### Getting Neighboring Geohashes

Retrieve neighboring geohashes surrounding a given geohash string, sorted clockwise from the top-left corner:

```python
# Get neighbors
neighbors = gh.neighbors(order=1)
print('Neighboring geohashes:', neighbors)
```

## API Reference

### Geohash

#### `__init__` method *(Internal Use Only)*

```python
__init__()
```

This internal constructor initializes a Geohash object with the default geohash value `'s0000000000'`. Direct usage is discouraged; use `init_with_lat_lng` or `init_with_geohash` for custom initialization.

#### `get_geohash` method

```python
get_geohash() -> str
```

Returns the current geohash string.

#### `set_geohash` method

```python
set_geohash(s: str)
```

Sets a new geohash string.

#### `encode_with_lat_lng` method

```python
encode_with_lat_lng(lat_lng: List[Union[float, int]], length: int = 11)
```

Encodes the provided latitude and longitude into a geohash string of the specified length.

#### `decode_to_interval` method

```python
decode_to_interval() -> List[Tuple[float, float]]
```

Decodes the geohash to its latitude and longitude interval.

#### `decode` method

```python
decode() -> List[float]
```

Decodes the geohash to the midpoint of its latitude and longitude interval.

#### `neighbors` method

```python
neighbors(order: int = 1) -> List[str]
```

Returns a list of neighboring geohashes around the current geohash.

## Technical Details

### Latitude and Longitude Normalization

- **Longitude Normalization**: Longitude values are wrapped within the range of -180 to 180 degrees using modular arithmetic. For example:
  - A longitude of `190` normalizes to `-170`.
  - A longitude of `-200` normalizes to `160`.

- **Latitude Normalization**: Latitude values are wrapped within the range of -90 to 90 degrees. If the value exceeds these bounds, it "bounces back" toward the center by reflecting over the boundary. For example:
  - A latitude of `-95` normalizes to `-85`.
  - A latitude of `100` normalizes to `80`.

This ensures realistic and accurate representation of geographic coordinates on the globe.

## License


This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This implementation is inspired by the Geohash algorithm explained in [this blog post](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0).

Feel free to contribute to this project by opening issues or submitting pull requests.
