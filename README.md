# Geohash Py

A comprehensive Python implementation of Geohash, designed for encoding and decoding geographic coordinates into a compact geohash string. This project is based on the Geohash algorithm described in [this blog post](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0).

## Features

- Encode geographical coordinates into a geohash string
- Decode a geohash string back to latitude and longitude coordinates
- Retrieve neighboring geohashes for a given geohash
- Input validation for coordinates and geohash strings
- Latitude and longitude normalization

## Installation

Clone the repository to your local machine:

```sh
git clone https://github.com/layla777/geohash_py.git
cd geohash_py
```

No additional dependencies are required since this is a pure Python implementation.

## Usage

Here's how you can use the `Geohash` class to encode and decode geohashes.

### Initializing a Geohash Object

You can initialize a `Geohash` object either by providing geographic coordinates or by providing a geohash string.

#### Using Latitude and Longitude

```python
from geohash import Geohash

# Initialize with latitude and longitude
lat_lng = [37.7749, -122.4194]  # San Francisco, CA
length = 8
geohash_obj = Geohash(lat_lng=lat_lng, length=length)
print("Generated geohash:", geohash_obj.get_geohash())
```

#### Using a Geohash String

```python
# Initialize with a geohash string
geohash_str = '9q8yy'
geohash_obj = Geohash(geohash=geohash_str)
print("Geohash:", geohash_obj.get_geohash())
```

### Encoding Coordinates

You can encode new coordinates into the existing geohash object:

```python
# Encode new coordinates
new_lat_lng = [34.0522, -118.2437]  # Los Angeles, CA
geohash_obj.encode_with_lat_lng(new_lat_lng, length)
print("New geohash:", geohash_obj.get_geohash())
```

### Decoding a Geohash

You can decode a geohash string back into latitude and longitude:

```python
# Decode geohash
lat_lng = geohash_obj.decode()
print("Decoded coordinates:", lat_lng)
```

### Getting Neighboring Geohashes

You can retrieve neighboring geohashes for a given geohash:

```python
# Get neighbors
neighbors = geohash_obj.neighbors(order=1)
print("Neighboring geohashes:", neighbors)
```

## API Reference

### Geohash

#### `__init__` method

```python
__init__(lat_lng: List[Union[float, int]] = None, length: int = 11, geohash: str = 's0000000000')
```

Initialize a Geohash object.

- `lat_lng`: List containing latitude and longitude.
- `length`: The desired length of the geohash string.
- `geohash`: A geohash string.

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

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

This implementation is inspired by the Geohash algorithm explained in [this blog post](http://mtcn.ko-me.com/%E9%96%A2%E6%95%B0%E3%80%81%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA/geohash%E9%96%A2%E6%95%B0).

Feel free to contribute to this project by opening issues or submitting pull requests.