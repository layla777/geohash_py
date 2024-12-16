from typing import List, Union, Tuple


class Geohash:
    """
    A class for working with geohash encoding and decoding.

    Geohash provides a compact way of representing geographic coordinates through a
    short alphanumeric string. This class offers utilities to encode, decode, and
    manipulate geohashes.

    Attributes:
        _geohash: The internal representation of the geohash string.

    Methods:
        - init_with_lat_lng: Initializes a geohash from latitude and longitude.
        - init_with_geohash: Initializes a geohash object from a geohash string.
        - encode_with_lat_lng: Encodes latitude and longitude into a geohash.
        - decode: Decodes a geohash back to latitude and longitude.
    """

    _BASE_32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    _BASE_32_RESULT = list(_BASE_32)
    _BASE_32_TABLE = {c: i for i, c in enumerate(_BASE_32)}

    def __init__(self, lat_lng: List[Union[float, int]] = None, length: int = 11, geohash: str = None):
        """
        Initialize the Geohash object.

        Args:
            lat_lng (List[Union[float, int]], optional): A list representing latitude and longitude as floats or integers.
                Both latitude and longitude must be within their respective valid ranges.
            length (int, optional): The desired length of the generated geohash (default is 11).
            geohash (str, optional): A valid geohash string.

        Raises:
            ValueError: If both lat_lng and geohash are specified or if invalid values are provided.
            TypeError: If 'lat_lng' or 'geohash' type is incorrect.
        """
        if lat_lng is not None and geohash is not None:
            raise ValueError('"lat_lng" and "geohash" cannot be specified at the same time.')
        if lat_lng is None and geohash is None:
            geohash = 's0000000000'
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

    def __str__(self):
        return f'Geohash: {self._geohash} | Lat/Lng: {self.decode()}'

    def __repr__(self):
        return f'<Geohash(geohash={self._geohash}, decoded={self.decode()})>'

    @staticmethod
    def _validate_length(length: int):
        """
        Validates the geohash length.

        Args:
            length (int): The desired geohash length.

        Raises:
            TypeError: If length is not an integer.
            ValueError: If length is less than 1.
        """
        if not isinstance(length, int):
            raise TypeError('"length" must be an integer.')
        if length < 1:
            raise ValueError('"length" must be a positive number and at least 1.')

    @classmethod
    def _validate_lat_lng(cls, lat_lng: List[Union[float, int]]):
        """
        Validates the latitude and longitude values.

        Args:
            lat_lng (List[Union[float, int]]): A list of two items representing latitude and longitude.

        Raises:
            TypeError: If lat_lng is not a list or its items are not float or int.
            ValueError: If the length of lat_lng is not 2.
        """
        if not isinstance(lat_lng, list):
            raise TypeError('"lat_lng" must be a list.')
        if len(lat_lng) != 2:
            raise ValueError('"lat_lng" must have 2 and only 2 items.')
        for item in lat_lng:
            if not isinstance(item, (float, int)):
                raise TypeError('Items of "lat_lng" must be float or integer.')

    @classmethod
    def _validate_geohash(cls, s: str):
        """
        Validates a geohash string.

        Args:
            s (str): The geohash string to validate.

        Raises:
            TypeError: If the geohash is not a string.
            ValueError: If the geohash is empty or contains invalid characters.
        """
        if not isinstance(s, str):
            raise TypeError('"geohash" must be a string.')
        if not s:
            raise ValueError('"geohash" must have at least one character.')
        for c in s:
            if c not in cls._BASE_32:
                raise ValueError('Invalid characters.')

    @classmethod
    def init_with_lat_lng(cls, lat_lng: List[Union[float, int]], length: int = 11):
        """
        Initializes a Geohash object using latitude and longitude with a specified precision (length).

        This method takes a pair of latitude and longitude values and generates a Geohash with
        the specified length (precision). Latitude and longitude values are normalized internally,
        so there is no need to validate their ranges manually. However, the input format
        must adhere to the specified requirements.

        Args:
            lat_lng (List[Union[float, int]]): A list containing exactly two items:
                                               the latitude (first element) and the longitude (second element).
                                               Both values must be either float or int.
            length (int, optional): The length (precision) of the generated geohash. Must be an integer
                                    greater than or equal to 1. Default is 11.

        Raises:
            TypeError: If `lat_lng` is not a list, or if any of its items are not float or int.
            ValueError: If `lat_lng` does not contain exactly two items.
            TypeError: If `length` is not an integer.
            ValueError: If `length` is less than 1.

        Returns:
            Geohash: A Geohash instance initialized with the given latitude/longitude values and precision (length).

        Examples:
            >>> gh = Geohash.init_with_lat_lng([42.583008, -5.625000], 12)
            >>> print(gh)
            Geohash: ezs420000001 | Lat/Lng: (42.583008063957095, -5.624999832361937)

        Notes:
            - This method ensures latitude and longitude values are normalized automatically.
            - The precision (`length`) affects the accuracy and size of the Geohash string.
        """

        return cls(lat_lng=lat_lng, length=length)

    @classmethod
    def init_with_geohash(cls, geohash: str):
        """
        Initializes a Geohash object using an existing geohash string.

        This method takes a geohash string as input, validates it, and creates a Geohash object
        based on the provided value. The validation ensures that the geohash string conforms
        to the correct format and contains only valid Base32 characters.

        Args:
            geohash (str): The geohash string to initialize the object.

        Raises:
            TypeError: If `geohash` is not a string.
            ValueError: If `geohash` is empty or contains invalid characters.

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

    def get_geohash(self) -> str:
        return self._geohash

    def set_geohash(self, s: str):
        self._validate_geohash(s)
        self._geohash = s

    def encode_with_lat_lng(self, lat_lng: List[Union[float, int]], length: int = 11) -> None:
        """
        Encodes a latitude and longitude pair into a geohash and sets it to the instance.

        Args:
            lat_lng (List[Union[float, int]]): A list containing latitude and longitude values.
                                               Each value must be either a float or an int.
            length (int, optional): The desired length (number of characters in the geohash, default is 11).
                                    Longer lengths increase precision (geographical granularity), while shorter lengths decrease precision.

        Returns:
            None: The geohash string is set to the instance's internal state.

        Raises:
            TypeError: If `lat_lng` is not a list, or any of its items are not of type `float` or `int`.
            ValueError: If `lat_lng` does not contain exactly two elements.

        Example:
            >>> gh = Geohash()  # Create a new instance of the Geohash class initialized with geohash 's0000000000'
            >>> gh.encode_with_lat_lng([37.7749, -122.4194], length=9)
            >>> print(gh)
            Geohash: 9q8yyk8yt | Lat/Lng: (37.774879932403564, -122.41938829421997)

            >>> gh.encode_with_lat_lng([51.5074, -0.1278], length=7)
            >>> print(gh)
            Geohash: gcpuvnj | Lat/Lng: (51.50733947753906, -0.1284027099609375)

            # Example of incorrect usage raising TypeError:
            >>> gh.encode_with_lat_lng('37.7749, -122.4194')  # Not a list
            TypeError: "lat_lng" must be a list.

            >>> gh.encode_with_lat_lng([37.7749, 'longitude'])  # Non-numeric type in list
            TypeError: Items of "lat_lng" must be float or integer.

            # Example of incorrect usage raising ValueError:
            >>> gh.encode_with_lat_lng([37.7749])  # Missing longitude
            ValueError: "lat_lng" must have 2 and only 2 items.
        """
        self._validate_lat_lng(lat_lng)
        self._validate_length(length)
        lat_lng[0] = self._normalize_lat(lat_lng[0])
        lat_lng[1] = self._normalize_angle_180(lat_lng[1])
        self._geohash = self._encode(lat_lng[0], lat_lng[1], length)

    def _encode(self, lat: float = 0, lng: float = 0, length: int = 11) -> str:
        """
        Encodes latitude and longitude into a geohash string.

        Args:
            lat (float): The latitude to encode.
            lng (float): The longitude to encode.
            length (int): The desired geohash length.

        Returns:
            str: The encoded geohash string.
        """
        lng_min, lng_max = -180.0, 180.0
        lat_min, lat_max = -90.0, 90.0
        bit_code = 0
        total_bits = length * 5
        is_lng = True

        for _ in range(total_bits):
            if is_lng:  # Longitude case
                mid = (lng_min + lng_max) / 2
                if lng < mid:
                    bit_code <<= 1
                    lng_max = mid
                else:
                    bit_code = (bit_code << 1) | 1
                    lng_min = mid
            else:  # Latitude case
                mid = (lat_min + lat_max) / 2
                if lat < mid:
                    bit_code <<= 1
                    lat_max = mid
                else:
                    bit_code = (bit_code << 1) | 1
                    lat_min = mid
            is_lng = not is_lng

        # Convert the integer bit sequence into a geohash string
        return ''.join(
            self._int_to_base_32((bit_code >> (5 * i)) & 0b11111)
            for i in reversed(range(length))
        )

    def decode_to_interval(self) -> tuple[list[float], list[float]]:
        """
        Decodes the current geohash into its corresponding latitude and longitude intervals.

        This method computes and returns the ranges of latitude and longitude that the current geohash represents.
        Each range is returned as a list containing two float values, [minimum, maximum],
        which define the geographical area encoded by the geohash.

        This is a standalone method and does not require any input parameters.

        Returns:
            tuple[list[float], list[float]]:
                - The first list represents the latitude interval: [min_latitude, max_latitude].
                - The second list represents the longitude interval: [min_longitude, max_longitude].

        Example:
            >>> gh = Geohash.init_with_geohash('ezs42e44yxpy')  # 11-character geohash
            >>> lat_range, lng_range = gh.decode_to_interval()
            >>> print(lat_range)  # Example: [42.59999793022871, 42.599998097866774]
            >>> print(lng_range)  # Example: [-5.5999914184212685, -5.599991083145142]
            >>> gh = Geohash.init_with_geohash('ezs42e')  # 6-character geohash
            >>> lat_range, lng_range = gh.decode_to_interval()
            >>> print(lat_range)  # Example: [42.5994873046875, 42.60498046875]
            >>> print(lng_range)  # Example: [-5.60302734375, -5.592041015625]

        Details:
            This function operates by converting the geohash string into its binary representation.
            Using this binary data, it iteratively reconstructs the latitude and longitude
            intervals by alternating each bit between:
              - Longitude bits (even positions)
              - Latitude bits (odd positions).
            For every bit, the method either splits the interval into the upper or lower half
            based on the bit's value (1 for upper, 0 for lower).

            Precision Limitations:
                At very high precision (long geohash strings, i.e., above 11 characters),
                the intervals for latitude and longitude become extremely small.
                Due to floating-point limitations in Python, negligible rounding errors or
                inaccuracies might arise. While these are minor, users should account for
                possible deviations when performing high-precision operations.
        """
        # Latitude and Longitude ranges
        lat_range = [-90.0, 90.0]
        lng_range = [-180.0, 180.0]

        # Precompute the bitstream
        bitstream = Geohash._geohash_to_bits(self._geohash)
        num_bits = len(self._geohash) * 5  # Total number of bits (5 bits per character)

        # Traverse the bits and update ranges
        is_even = True
        for bit_position in range(num_bits - 1, -1, -1):  # Iterate from MSB to LSB
            bit = (bitstream >> bit_position) & 1  # Extract the current bit
            range_ref = lng_range if is_even else lat_range
            mid = (range_ref[0] + range_ref[1]) / 2
            if bit == 1:
                range_ref[0] = mid  # Update lower bound
            else:
                range_ref[1] = mid  # Update upper bound

            is_even = not is_even  # Alternate between lat/lng

        return lat_range, lng_range

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
            TypeError: If `order` is not a natural number (integer greater than or equal to 1).

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
        if not isinstance(order, int) or order < 1:
            raise TypeError('"order" must be a natural number.')

        # Retrieve latitude and longitude intervals as well as their center and width
        interval_lat, interval_lng = self.decode_to_interval()
        delta_lat = interval_lat[1] - interval_lat[0]  # Latitude interval width
        delta_lng = interval_lng[1] - interval_lng[0]  # Longitude interval width
        lat = (interval_lat[0] + interval_lat[1]) / 2  # Center latitude
        lng = (interval_lng[0] + interval_lng[1]) / 2  # Center longitude

        # Pre-compute relative positions for neighbors based on the specified order
        relative_positions = [
            (i, j) for i in range(-order, order + 1)
            for j in range(-order, order + 1)
            if not (i == 0 and j == 0)  # Exclude the current position
        ]

        geohashes = []  # To store all neighboring geohashes

        for i, j in relative_positions:
            # Adjust latitude and longitude using the relative position
            lat_tmp = Geohash._normalize_lat(lat + delta_lat * i)
            lng_tmp = Geohash._normalize_angle_180(lng + delta_lng * j)

            # Encode the adjusted latitude and longitude into a geohash
            geohashes.append(self._encode(lat_tmp, lng_tmp, len(self)))

        return geohashes

    """
    Contains utility methods for normalization, conversion, and rounding.
    """
    @staticmethod
    def _normalize_angle_180(lng: float) -> float:
        lng_is_negative = lng < 0
        lng %= 360
        return lng - 360 if lng > 180 else -lng if lng_is_negative else lng

    @staticmethod
    def _normalize_lat(lat: float) -> float:
        lat = Geohash._normalize_angle_180(lat)
        return 180 - lat if lat > 90 else (-180 - lat if lat < -90 else lat)

    @staticmethod
    def _bits_to_int(bits: List[str]) -> int:
        return int(''.join(bits), 2)

    @staticmethod
    def _int_to_base_32(v: int) -> str:
        return Geohash._BASE_32_RESULT[v]

    @staticmethod
    def _base_32_to_int(c: str) -> int:
        return Geohash._BASE_32_TABLE[c]

    @staticmethod
    def _round(val: float, digit: int = 0) -> float:
        p = 10 ** digit
        return (val * p * 2 + 1) // 2 / p

    @staticmethod
    def _geohash_to_bits(geohash: str) -> int:
        """
        Converts a geohash string into a single integer representing bits.

        Each character in the geohash is converted to a 5-bit binary representation,
        and these are combined to form a single integer.

        Args:
            geohash (str): The input geohash string.

        Returns:
            int: An integer where the binary representation encodes the geohash bits.
        """
        bitstream = 0  # Initialize bitstream as an integer
        for c in geohash:
            value = Geohash._base_32_to_int(c)  # Convert to 5-bit value
            bitstream = (bitstream << 5) | value  # Left-shift and append the 5-bit value
        return bitstream
