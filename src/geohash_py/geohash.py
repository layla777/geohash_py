import warnings
from functools import lru_cache
from typing import List, Optional, Tuple, Union

from bitarray import bitarray

from .geohash_exceptions import GeohashTypeError, GeohashValueError
from .geohash_warnings import GeohashWarning


class Geohash:
    """
    A class for working with geohash encoding and decoding.

    Geohash provides a compact way of representing geographic coordinates through a
    short alphanumeric string. This class offers utilities to encode, decode, and
    manipulate geohashes.

    Attributes:
        _geohash: The internal representation of the geohash string.

    Methods:
        - init_with_lat_lng/from_lat_lng: Initializes a geohash from latitude and longitude.
        - init_with_geohash/from_geohash: Initializes a geohash object from a geohash string.
        - encode_with_lat_lng: Encodes latitude and longitude into a geohash.
        - decode: Decodes a geohash back to latitude and longitude.
        - decode_to_interval: Decodes a geohash into latitude and longitude intervals,
          providing the bounding box of the geohash.
        - neighbors: Retrieves the geohashes of the neighboring cells around the current
          geohash, useful for spatial queries.
        Getter:
            - geohash: Retrieves the current geohash string.
            - get_geohash (deprecated): Retrieves the current geohash string. Use 'geohash' property instead.
            - precision: Retrieves the precision (length) of the geohash string.
        Setter:
            - geohash: Sets a new geohash string, validating its format before updating the value.
            - set_geohash (deprecated): Sets a new geohash string. Use 'geohash' property instead.
    """

    _DEFAULT_GEOHASH_LENGTH = 11
    _DEFAULT_GEOHASH = 's0000000000'

    _BASE_32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    # Precomputed dictionary for 5-bit to Base32 character mapping
    _BIT_TO_CHAR_MAP = {
        i: char
        for i, char in enumerate(_BASE_32)
    }
    _BASE_32_TABLE = {char: bitarray(f'{i:05b}') for i, char in enumerate(_BASE_32)}

    def __init__(self, lat_lng: Optional[List[Union[float, int]]] = None, length: int = _DEFAULT_GEOHASH_LENGTH,
                 geohash: Optional[str] = None) -> None:
        """
        Initialize the Geohash object.

        Args:
            lat_lng (List[Union[float, int]], optional): A list representing latitude and longitude as floats or integers.
                Both latitude and longitude must be within their respective valid ranges.
            length (int, optional): The desired length of the generated geohash (default is `_DEFAULT_GEOHASH_LENGTH`).
            geohash (str, optional): A valid geohash string.

        Raises:
            GeohashValueError:
                - If both lat_lng and geohash are specified or if invalid values are provided.
            GeohashTypeError:
                - If 'lat_lng' or 'geohash' type is incorrect.
        """
        if lat_lng is not None and geohash is not None:
            raise GeohashValueError("'lat_lng' and 'geohash' cannot be specified at the same time.")

        if lat_lng is None and geohash is None:
            warnings.warn(
                f"No latitude/longitude or geohash provided. Default geohash '{Geohash._DEFAULT_GEOHASH}' "
                'will be used. This may lead to unexpected results if not intentional.',
                category=GeohashWarning
            )
            geohash = self._DEFAULT_GEOHASH

        if lat_lng is not None:
            Geohash._validate_lat_lng(lat_lng)
            self._validate_length(length)
            lat_lng[0] = self._normalize_lat(lat_lng[0])
            lat_lng[1] = self._normalize_angle_180(lat_lng[1])
            self._geohash = self._encode(lat_lng[0], lat_lng[1], length)
        else:
            self._validate_geohash(geohash)
            self._geohash = geohash

    def __len__(self) -> int:
        return len(self._geohash)

    # Alias for __len__ to represent the precision of the geohash.
    _precision = __len__

    @property
    def precision(self) -> int:
        return self._precision()

    def __str__(self) -> str:
        return f'Geohash: {self._geohash} | Lat/Lng: {self.decode()}'

    def __repr__(self) -> str:
        return f'<Geohash(geohash={self._geohash}, decoded={self.decode()})>'

    @staticmethod
    def _resolve_length_and_precision(length: Union[int, None], precision: Union[int, None]) -> int:
        # Resolve length and precision conflict
        if length is None and precision is None:
            return Geohash._DEFAULT_GEOHASH_LENGTH  # Default length if none are provided
        elif length is not None and precision is not None:
            raise GeohashValueError("Both 'length' and 'precision' cannot be provided at the same time.")
        else:
            return length or precision  # Use 'length' if provided; otherwise, fall back to 'precision'

    @staticmethod
    def _validate_length(length: int):
        """
        Validates the geohash length.

        Args:
            length (int): The desired geohash length.

        Raises:
            GeohashTypeError:
                - If length is not an integer.
            GeohashValueError:
                - If length is less than 1.
        """
        if not isinstance(length, int):
            raise GeohashTypeError("'length' must be an integer.")
        if length < 1:
            raise GeohashValueError("'length' must be a positive number and at least 1.")

    @classmethod
    def _validate_lat_lng(cls, lat_lng: List[Union[float, int]]):
        """
        Validates the latitude and longitude values.

        Args:
            lat_lng (List[Union[float, int]]): A list of two items representing latitude and longitude.

        Raises:
            GeohashTypeError:
                - If lat_lng is not a list or its items are not float or int.
            GeohashValueError:
                - If the length of lat_lng is not 2.
        """
        if not isinstance(lat_lng, list):
            raise GeohashTypeError("'lat_lng' must be a list.")
        if len(lat_lng) != 2:
            raise GeohashValueError("'lat_lng' must have 2 and only 2 items.")
        for item in lat_lng:
            if not isinstance(item, (float, int)):
                raise GeohashTypeError("Items of 'lat_lng' must be float or integer.")

    @classmethod
    def _validate_geohash(cls, s: str):
        """
        Validates a geohash string.

        Args:
            s (str): The geohash string to validate.

        Raises:
            GeohashTypeError:
                - If the geohash is not a string.
            GeohashValueError:
                - If the geohash is empty or contains invalid characters.
        """
        if not isinstance(s, str):
            raise GeohashTypeError("'geohash' must be a string.")
        if not s:
            raise GeohashValueError("'geohash' must have at least one character.")
        for c in s:
            if c not in cls._BASE_32:
                raise GeohashValueError('Invalid characters.')

    @classmethod
    def init_with_lat_lng(cls, lat_lng: List[Union[float, int]], length: Union[int, None] = None, *,
                          precision: Union[int, None] = None):
        """
        Initializes a Geohash object using latitude and longitude with a specified precision.

        This method takes a pair of latitude and longitude values and generates a Geohash with
        the specified precision. Latitude and longitude values are normalized internally,
        so there is no need to validate their ranges manually. However, the input format
        must adhere to the specified requirements.

        This method is for developers with a love for descriptive, expressive,
        and nostalgic method names inspired by Smalltalk, Objective-C, and Swift.

        Args:
            lat_lng (List[Union[float, int]]): A list containing exactly two items:
                                               the latitude (first element) and the longitude (second element).
                                               Both values must be either float or int.
            length (int, optional): The desired length (number of characters in the geohash, default is `_DEFAULT_GEOHASH_LENGTH`).
                                    Longer lengths increase precision (geographical granularity), while shorter lengths
                                    decrease precision.
            precision (int, optional): An alternative way to specify the precision of the geohash.
                                       Must be an integer greater than or equal to 1.

        Raises:
            GeohashTypeError:
                - If `lat_lng` is not a list, or if any of its items are not float or int.
                - If `lat_lng` does not contain exactly two items.
            GeohashValueError:
                - If `length` is not an integer or less than 1.
                - If `precision` is not an integer or less than 1.
                - If both `length` and `precision` are specified.

        Returns:
            Geohash: A Geohash instance initialized with the given latitude/longitude values and length/precision.

        Examples:
        >>> gh = Geohash.init_with_lat_lng([35, 135], length=5)
        >>> print(gh)
        Geohash: ezs42 | Lat/Lng: (35.000014305114746, 135.0000035762787)

        >>> gh = Geohash.init_with_lat_lng([35, 135], precision=8)
        >>> print(gh)
        Geohash: ezs42gxs | Lat/Lng: (35.000056743621826, 135.00001430511475)

        >>> Geohash.init_with_lat_lng([35, 135], length=5, precision=8)
        Traceback(most recent call last):
        ...
        GeohashValueError: Both 'length' and 'precision' cannot be provided at the same time.

        Notes:
            - Latitude and longitude values are normalized automatically.
            - The precision (either via `length` or `precision`) affects the accuracy and size of the Geohash string.
            - Specify either `length` or `precision`, but not both. Doing so will raise a `GeohashValueError`.
        """

        return cls(lat_lng=lat_lng, length=Geohash._resolve_length_and_precision(length, precision))

    # A Pythonic style alias for init_with_lat_lng. You know, for those who prefer their
    # method names short, modern, pragmatic, and to-the-point. It does the exact same thing,
    # just without the nostalgic flair.
    from_lat_lng = init_with_lat_lng

    @classmethod
    def init_with_geohash(cls, geohash: str):
        """
        Initializes a Geohash object using an existing geohash string.

        This method takes a geohash string as input, validates it, and creates a Geohash object
        based on the provided value. The validation ensures that the geohash string conforms
        to the correct format and contains only valid Base32 characters.

        This method is for developers with an eye for classical, verbose, and expressive
        method names. Inspired by the descriptive elegance of languages like Smalltalk,
        Objective-C, and Swift, this one's for those who love their methods to tell a story.

        Args:
            geohash (str): The geohash string to initialize the object.

        Raises:
            GeohashTypeError:
                - If `geohash` is not a string.
            GeohashValueError:
                - If `geohash` is empty or contains invalid characters.

        Returns:
            Geohash: A Geohash instance initialized from the given geohash string.

        Examples:
            >>> gh = Geohash.init_with_geohash('ezs42')
            >>> print(gh)
            Geohash: ezs42 | Lat/Lng: (42.60498046875, -5.60302734375)

        Notes:
            - The geohash string must use valid Base32 characters (letters and digits).
            - Unlike other initialization methods, this directly sets up the object
              based on the provided geohash without additional transformations.
        """
        return cls(geohash=geohash)

    # Oh, you're one of *those* people who prefer shorter, Pythonic names?
    # Fine, here's from_geohash—our less nostalgic, more minimalist alias for init_with_geohash.
    from_geohash = init_with_geohash

    def get_geohash(self) -> str:
        warnings.warn(
            'get_geohash() is deprecated and will be removed in a future version. '
            "Use the 'geohash' property instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._geohash

    @property
    def geohash(self) -> str:
        return self._geohash

    def set_geohash(self, s: str):
        warnings.warn(
            'set_geohash() is deprecated and will be removed in a future version. '
            "Use the 'geohash' property instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._validate_geohash(s)
        self._geohash = s

    @geohash.setter
    def geohash(self, s: str):
        self._validate_geohash(s)
        self._geohash = s

    def encode_with_lat_lng(self, lat_lng: List[Union[float, int]], length: Union[int, None] = None, *,
                            precision: Union[int, None] = None) -> None:
        """
        Encodes a latitude and longitude pair into a geohash and sets it to the instance.

        Args:
            lat_lng (List[Union[float, int]]): A list containing latitude and longitude values.
                                               Each value must be either a float or an int.
            length (int, optional): The desired length (number of characters in the geohash, default is `_DEFAULT_GEOHASH_LENGTH`).
                                    Longer lengths increase precision (geographical granularity), while shorter lengths decrease precision.
            precision (int, optional): An alternative way to specify the precision of the geohash.
                                       Must be an integer greater than or equal to 1.

        Raises:
            GeohashTypeError:
                - If `lat_lng` is not a list, or any of its items are not of type `float` or `int`.
            GeohashValueError:
                - If `lat_lng` does not contain exactly two elements.
                - If both `length` and `precision` are specified.

        Returns:
            None: The geohash string is set to the instance's internal state.

        Example:
            >>> gh = Geohash()  # Create a new instance of the Geohash class initialized with geohash 's0000000000'
            >>> gh.encode_with_lat_lng([37.7749, -122.4194], length=9)
            >>> print(gh)
            Geohash: 9q8yyk8yt | Lat/Lng: (37.774879932403564, -122.41938829421997)

            >>> gh.encode_with_lat_lng([51.5074, -0.1278], length=7)
            >>> print(gh)
            Geohash: gcpuvnj | Lat/Lng: (51.50733947753906, -0.1284027099609375)

            >>> gh.encode_with_lat_lng([37.7749, -122.4194], precision=6)
            >>> print(gh)
            Geohash: 9q8yyk | Lat/Lng: (37.77490425109863, -122.41935729980469)

            # Example of incorrect usage raising GeohashTypeError:
            >>> gh.encode_with_lat_lng('37.7749, -122.4194')  # Not a list
            GeohashTypeError: "lat_lng" must be a list.

            >>> gh.encode_with_lat_lng([37.7749, 'longitude'])  # Non-numeric type in list
            GeohashTypeError: Items of "lat_lng" must be float or integer.

            # Example of incorrect usage raising GeohashValueError:
            >>> gh.encode_with_lat_lng([37.7749])  # Missing longitude
            GeohashValueError: "lat_lng" must have 2 and only 2 items.

            >>> gh.encode_with_lat_lng([37.7749, -122.4194], length=7, precision=5)
            Traceback (most recent call last):
                ...
            GeohashValueError: Both 'length' and 'precision' cannot be provided at the same time.
        """
        self._validate_lat_lng(lat_lng)
        length = Geohash._resolve_length_and_precision(length, precision)
        self._validate_length(length)
        lat_lng[0] = self._normalize_lat(lat_lng[0])
        lat_lng[1] = self._normalize_angle_180(lat_lng[1])
        self._geohash = self._encode(lat_lng[0], lat_lng[1], length=length)

    @staticmethod
    def _encode(lat: float = 0, lng: float = 0, length: int = _DEFAULT_GEOHASH_LENGTH) -> str:
        """
        Encodes latitude and longitude into a geohash string.

        Args:
            lat (float): The latitude to encode.
            lng (float): The longitude to encode.
            length (int): The desired geohash length.

        Returns:
            str: The encoded geohash string.
        """
        # Initialize range boundaries
        lng_lat_range = [[-180.0, 180.0], [-90.0, 90.0]]
        lng_lat = [lng, lat]

        # Pre-allocate bitarray
        total_bits = length * 5
        bits = bitarray(total_bits)  # Reserve size beforehand

        for i in range(total_bits):
            lng_lat_ref = lng_lat_range[lng_lat_index := i & 1]
            b = lng_lat[lng_lat_index] >= (mid := (lng_lat_ref[0] + lng_lat_ref[1]) / 2)
            bits[i] = b  # Directly assign without append
            lng_lat_ref[b ^ 1] = mid

        # Directly calculate Base32 using integer conversion
        return ''.join(
            Geohash._BIT_TO_CHAR_MAP[
                (bits[i] << 4) + (bits[i + 1] << 3) + (bits[i + 2] << 2) + (bits[i + 3] << 1) + bits[i + 4]
                ]
            for i in range(0, total_bits, 5)
        )

    @lru_cache(maxsize=1024)
    def decode_to_interval(self) -> Tuple[List[float], List[float]]:
        """
        Decodes the current geohash into latitude and longitude intervals.

        This version uses the bitarray returned by `_geohash_to_bits` for efficiency.

        Returns:
            Tuple[List[float], List[float]]:
                - Latitude interval: [min_latitude, max_latitude]
                - Longitude interval: [min_longitude, max_longitude]
        """
        # Latitude and Longitude ranges
        lat_lng_range = [[-90.0, 90.0], [-180.0, 180.0]]

        # Retrieve the bitarray representation of the geohash
        bits = Geohash._geohash_to_bits(self._geohash)

        # Traverse the bits and update ranges
        for i, bit in enumerate(bits):
            range_ref = lat_lng_range[(i & 1) ^ 1]  # Alternate between longitude and latitude
            mid = (range_ref[0] + range_ref[1]) / 2
            range_ref[bit ^ 1] = mid

        return lat_lng_range[0], lat_lng_range[1]

    def decode(self) -> Tuple[float, float]:
        """
        Decodes the current geohash into its corresponding latitude and longitude.

        This method computes the central latitude and longitude of the region
        represented by the geohash. Internally, it uses the `decode_to_interval` method
        to calculate the intervals for latitude and longitude, and then determines
        the midpoint of these intervals. The returned latitude and longitude are
        computed with precision based on the length of the geohash and Python's
        floating-point representation.

        Returns:
            List[float]: A list of two values:
                - The first value is the decoded latitude (float).
                - The second value is the decoded longitude (float).

        Example:
            >>> gh = Geohash.init_with_geohash('ezs42e44yxpy')  # 11-character geohash
            >>> decoded = gh.decode()
            >>> print(decoded)  # Example output: [42.599998, -5.59999]

            >>> gh = Geohash.init_with_geohash('ezs42e')  # 6-character geohash
            >>> decoded = gh.decode()
            >>> print(decoded)  # Example output: [42.6, -5.6]

        Details:
            - The central latitude and longitude are calculated by averaging
              the minimum and maximum values of the latitude and longitude intervals.
            - The precision of the output depends on the length of the geohash:
                - Longer geohashes (e.g., 11 characters) yield more precise results.
                - Shorter geohashes (e.g., 6 characters) yield less precise results.
            - Python's floating-point accuracy may cause minor rounding errors in
              high-precision operations. These errors are negligible for most use cases.
        """
        interval_lat, interval_lng = self.decode_to_interval()

        return (interval_lat[0] + interval_lat[1]) / 2, (interval_lng[0] + interval_lng[1]) / 2

    @staticmethod
    def _precompute_normalized_positions(lat, lng, delta_lat, delta_lng, relative_positions):
        """
        Precomputes all normalized latitude and longitude positions
        to reduce repeated calls to normalization functions.

        Args:
            lat (float): Center latitude of the geohash.
            lng (float): Center longitude of the geohash.
            delta_lat (float): Latitude interval width.
            delta_lng (float): Longitude interval width.
            relative_positions (List[Tuple[int, int]]): Relative positions for neighbors.

        Returns:
            List[Tuple[float, float]]: Normalized latitude and longitude values for each position.
        """
        return [
            [lat + delta_lat * i, lng + delta_lng * j]
            for i, j in relative_positions
        ]

    @staticmethod
    @lru_cache(maxsize=1024)
    def generate_relative_positions(order: int) -> List[Tuple[int, int]]:
        """
        Generates the relative positions for a given order using caching.
        This ensures we only compute each order's grid once.
        """
        return [
            (i, j)
            for i in range(-order, order + 1)
            for j in range(-order, order + 1)
            if not (i == 0 and j == 0)
        ]

    @lru_cache(maxsize=2048)
    def neighbors(self, order: int = 1) -> List[str]:
        """
        Computes the neighboring geohashes around the current geohash.

        Args:
            order (int, optional): The distance from the current geohash (default is 1).
                If `order=1`, the neighbors within a distance of 1 from the current geohash
                are included. If `order=2`, the neighbors within a distance of 2 are included.

        Returns:
            List[str]: A list of neighboring geohashes.

        Raises:
            GeohashTypeError:
                - If `order` is not a natural number (integer greater than or equal to 1).

        Examples:
            >>> gh = Geohash.init_with_lat_lng([37.7749, -122.4194], length=9)
            >>> neighbors = gh.neighbors(order=1)
            >>> print(neighbors)
            ['9q8yyk8yk', '9q8yyk8ym', '9q8yyk8yq', '9q8yyk8ys', '9q8yyk8yw', '9q8yyk8yu', '9q8yyk8yv', '9q8yyk8yy']

            >>> neighbors = gh.neighbors(order=2)
            >>> print(neighbors[:5])  # Print only the first 5 neighbors for brevity
            ['9q8yyk8y5', '9q8yyk8yh', '9q8yyk8yj', '9q8yyk8yn', '9q8yyk8yp']

        Details:
            The `relative_positions` list computes all neighbor offsets within the specified
            `order`, excluding the position of the current geohash itself. It generates a grid
            of relative (i, j) coordinates where:

            - i and j range from -order to +order.
            - The origin (0, 0) is excluded to ensure only the true neighbors are selected.
        """
        if not isinstance(order, int):
            raise GeohashTypeError("'order' must be a natural number (integer greater than 0).")
        if order < 1:
            raise GeohashValueError("'order' must be a natural number (integer greater than 0).")

        # Retrieve latitude and longitude intervals as well as their center and width
        interval_lat, interval_lng = self.decode_to_interval()
        delta_lat = interval_lat[1] - interval_lat[0]
        delta_lng = interval_lng[1] - interval_lng[0]
        lat = (interval_lat[0] + interval_lat[1]) / 2
        lng = (interval_lng[0] + interval_lng[1]) / 2

        # Pre-compute relative positions for neighbors based on the specified order
        relative_positions = self.generate_relative_positions(order)

        precomputed_positions = Geohash._precompute_normalized_positions(
            lat, lng, delta_lat, delta_lng, relative_positions
        )

        geohashes = [
            self._encode(norm_lat, norm_lng, len(self))
            for norm_lat, norm_lng in precomputed_positions
        ]

        return geohashes

    """
    Contains utility methods for normalization, conversion, and rounding.
    """

    @staticmethod
    @lru_cache(maxsize=1024)
    def _normalize_angle_180(lng: float) -> float:
        is_negative = lng < 0  # Extract sign information
        lng = lng % 360  # Normalize to [0, 360)
        if lng > 180:
            lng -= 360  # Shift angles > 180
        if is_negative and lng == 180:
            return -180  # Handle edge case for -180
        return lng

    @staticmethod
    @lru_cache(maxsize=1024)
    def _normalize_lat(lat: float) -> float:
        lat = Geohash._normalize_angle_180(lat)
        return 180 - lat if lat > 90 else (-180 - lat if lat < -90 else lat)

    @staticmethod
    def _round(val: float, digit: int = 0) -> float:
        p = 10 ** digit
        return (val * p * 2 + 1) // 2 / p

    @staticmethod
    @lru_cache(maxsize=1024)
    def _geohash_to_bits(geohash: str) -> bitarray:
        """
        Converts a geohash string into a bitarray.

        Args:
            geohash (str): The input geohash string.

        Returns:
            bitarray: A bitarray where each bit represents a part of the geohash.
        """
        result = bitarray()  # Initialize an empty bitarray
        base_32_table = Geohash._BASE_32_TABLE  # Retrieve the _BASE_32_TABLE

        # Extend with each character's corresponding bitarray
        for c in geohash:
            result.extend(base_32_table[c])  # Extend the bitarray directly

        return result
