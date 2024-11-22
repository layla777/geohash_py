from math import log10
from typing import List, Tuple, Union


class Geohash:
    """
    Class for generating and decoding Geohash.
    """

    _BASE_32 = '0123456789bcdefghjkmnpqrstuvwxyz'

    def __init__(self, lat_lng: List[Union[float, int]] = None, length: int = 11, geohash: str = 's0000000000'):
        """
        Initialize the Geohash object.
        """
        if lat_lng:
            self._validate_lat_lng(lat_lng)
            self._validate_length(length)
            lat_lng[0] = self._normalize_lat(lat_lng[0])
            lat_lng[1] = self._normalize_angle_180(lat_lng[1])
            self._geohash = self._encode(lat_lng[0], lat_lng[1], length)
        elif geohash:
            self._validate_geohash(geohash)
            self._geohash = geohash
        else:
            raise TypeError('Invalid arguments.')

    def __len__(self) -> int:
        return len(self._geohash)

    @staticmethod
    def _validate_length(length: int):
        if not isinstance(length, int):
            raise TypeError('"length" must be an integer.')
        if length < 1:
            raise ValueError('"length" must be a positive number and at least 1.')

    @classmethod
    def _validate_lat_lng(cls, lat_lng: List[Union[float, int]]):
        if not isinstance(lat_lng, list):
            raise TypeError('"lat_lng" must be a list.')
        if len(lat_lng) != 2:
            raise ValueError('"lat_lng" must have 2 and only 2 items')
        for item in lat_lng:
            if not isinstance(item, (float, int)):
                raise TypeError('Items of "lat_lng" must be float or integer.')

    @classmethod
    def _validate_geohash(cls, s: str):
        if not isinstance(s, str):
            raise TypeError('"geohash" must be a string.')
        if not s:
            raise ValueError('"geohash" must have at least one character.')
        for c in s:
            if c not in cls._BASE_32:
                raise ValueError('Invalid characters.')

    @classmethod
    def init_with_lat_lng(cls, lat_lng: List[Union[float, int]], length: int = 11):
        return cls(lat_lng=lat_lng, length=length)

    @classmethod
    def init_with_geohash(cls, geohash: str):
        return cls(geohash=geohash)

    def get_geohash(self) -> str:
        return self._geohash

    def set_geohash(self, s: str):
        self._validate_geohash(s)
        self._geohash = s

    def encode_with_lat_lng(self, lat_lng: List[Union[float, int]], length: int = 11):
        self._validate_lat_lng(lat_lng)
        self._validate_length(length)
        lat_lng[0] = self._normalize_lat(lat_lng[0])
        lat_lng[1] = self._normalize_angle_180(lat_lng[1])
        self._geohash = self._encode(lat_lng[0], lat_lng[1], length)

    def _encode(self, lat: float = 0, lng: float = 0, length: int = 11) -> str:
        lat_min, lat_max = -90.0, 90.0
        lng_min, lng_max = -180.0, 180.0
        bit_codes = []

        for _ in range(length * 5):
            lng_mid = (lng_min + lng_max) / 2
            if lng < lng_mid:
                bit_codes.append('0')
                lng_max = lng_mid
            else:
                bit_codes.append('1')
                lng_min = lng_mid

            lat_mid = (lat_min + lat_max) / 2
            if lat < lat_mid:
                bit_codes.append('0')
                lat_max = lat_mid
            else:
                bit_codes.append('1')
                lat_min = lat_mid

        return ''.join(self._int_to_base_32(self._bits_to_int(bit_codes[i * 5:i * 5 + 5])) for i in range(length))

    def decode_to_interval(self) -> List[Tuple[float, float]]:
        lat = [-90.0, 90.0]
        lng = [-180.0, 180.0]
        is_even = True
        for c in self._geohash:
            v = self._base_32_to_int(c)
            for mask in [2 ** j for j in reversed(range(5))]:
                if is_even:
                    lng = [sum(lng) / 2, lng[1]] if v & mask else [lng[0], sum(lng) / 2]
                else:
                    lat = [sum(lat) / 2, lat[1]] if v & mask else [lat[0], sum(lat) / 2]
                is_even = not is_even
        return [lat, lng]

    def decode(self) -> List[float]:
        interval_lat, interval_lng = self.decode_to_interval()
        places_lat = max(1, -self._round(log10(interval_lat[1] - interval_lat[0])) - 1)
        places_lng = max(1, -self._round(log10(interval_lng[1] - interval_lng[0])) - 1)
        lat = self._round(sum(interval_lat) / 2, places_lat)
        lng = self._round(sum(interval_lng) / 2, places_lng)
        return [lat, lng]

    def neighbors(self, order: int = 1) -> List[str]:
        if not isinstance(order, int) or order < 1:
            raise TypeError('"order" must be a natural number.')

        interval_lat, interval_lng = self.decode_to_interval()
        delta_lat = interval_lat[1] - interval_lat[0]
        delta_lng = interval_lng[1] - interval_lng[0]

        lat = sum(interval_lat) / 2
        lng = sum(interval_lng) / 2

        geohashes = []

        for i in range(-order, order + 1):
            for j in range(-order, order + 1):
                if i == 0 and j == 0:
                    continue

                lat_tmp = lat + delta_lat * i
                lat_tmp = 180 - lat_tmp if lat_tmp > 90 else (-180 - lat_tmp if lat_tmp < -90 else lat_tmp)

                lng_tmp = lng + delta_lng * j
                lng_tmp = lng_tmp % 360 if lng_tmp < -180 else (lng_tmp % 360 if lng_tmp > 180 else lng_tmp)

                geohashes.append(self._encode(lat_tmp, lng_tmp, len(self)))

        return geohashes

    @staticmethod
    def _normalize_angle_180(lng: float) -> float:
        lng %= 360
        return lng - 360 if lng > 180 else lng

    @staticmethod
    def _normalize_lat(lat: float) -> float:
        lat = Geohash._normalize_angle_180(lat)
        return 180 - lat if lat > 90 else (-180 - lat if lat < -90 else lat)

    @staticmethod
    def _bits_to_int(bits: List[str]) -> int:
        return int(''.join(bits), 2)

    def _int_to_base_32(self, v: int) -> str:
        return self._BASE_32[v]

    def _base_32_to_int(self, c: str) -> int:
        return self._BASE_32.index(c)

    @staticmethod
    def _round(val: float, digit: int = 0) -> float:
        p = 10 ** digit
        return (val * p * 2 + 1) // 2 / p
