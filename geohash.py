from math import log10


class Geohash:
    _BASE_32 = '0123456789bcdefghjkmnpqrstuvwxyz'

    def __init__(self, **kwargs):
        if kwargs == {}:
            self._geohash = 's0000000000'
            return

        if '_lat_lng' in kwargs and '_length' in kwargs:
            lat_lng = kwargs.get('_lat_lng', [])
            length = kwargs.get('_length', 11)

            lat_lng[0] = self._normalize_lat(lat_lng[0])
            lat_lng[1] = self._normalize_angle_180(lat_lng[1])

            self._geohash = self._encode(lat_lng[0], lat_lng[1], length)
            return

        if '_geohash' in kwargs:
            self._geohash = kwargs.get('_geohash')
            return

        raise TypeError('Invalid argument.')

    def __len__(self):
        return len(self._geohash)

    @staticmethod
    def _validate_len(length):
        if not isinstance(length, int):
            raise TypeError('"length" must be an integer.')
        if length < 0:
            raise ValueError('"length" must be a positive number.')

    @classmethod
    def _validate_lat_lng(cls, lat_lng):
        if not isinstance(lat_lng, list):
            raise TypeError('"lat_lng" must be a list.')

        if len(lat_lng) != 2:
            raise ValueError('"lat_lng" must have 2 and only 2 items')

        for item in lat_lng:
            if not isinstance(item, float) and not isinstance(item, int):
                raise TypeError('Items of "lat_lng" must be float or integer.')

    @classmethod
    def _validate_geohash(cls, s):
        if not isinstance(s, str):
            raise TypeError('"geohash" must be a string.')

        if s == '':
            raise ValueError('"geohash" must have at least one character.')

        for c in s:
            if c not in cls._BASE_32:
                raise ValueError('Invalid characters.')

    @classmethod
    def init_with_lat_lng(cls, lat_lng, length=11):
        cls._validate_lat_lng(lat_lng)
        cls._validate_len(length)

        return cls(_lat_lng=lat_lng, _length=length)

    @classmethod
    def init_with_geohash(cls, geohash):
        cls._validate_geohash(geohash)

        return cls(_geohash=geohash)

    def geohash(self):
        return self._geohash

    def set(self, s):
        self._validate_geohash(s)
        self._geohash = s

    def encode_with_lat_lng(self, lat_lng, length=11):
        self._validate_lat_lng(lat_lng)
        self._validate_len(length)

        lat_lng[0] = self._normalize_lat(lat_lng[0])
        lat_lng[1] = self._normalize_angle_180(lat_lng[1])

        self._geohash = self._encode(lat_lng[0], lat_lng[1], length)

    def _encode(self, lat=0, lng=0, length=11):
        lat_min = -90.0
        lat_max = 90.0
        lng_min = -180.0
        lng_max = 180.0

        bit_codes = []
        for i in range(0, length * 5 + 1):
            lng_c = (lng_min + lng_max) / 2
            if lng < lng_c:
                bit_codes.append('0')
                lng_max = lng_c
            else:
                bit_codes.append('1')
                lng_min = lng_c

            lat_c = (lat_min + lat_max) / 2
            if lat < lat_c:
                bit_codes.append('0')
                lat_max = lat_c
            else:
                bit_codes.append('1')
                lat_min = lat_c

        geohash_codes = []
        for i in range(0, length):
            sub_bits = bit_codes[i * 5:i * 5 + 5]
            geohash_codes.append(
                self._int_to_base_32(self._bits_to_int(sub_bits)))

        return ''.join(geohash_codes)

    def decode_to_interval(self):
        lat = [-90.0, 90.0]
        lng = [-180.0, 180.0]

        length = self.__len__()

        is_even = True
        for i in range(0, length):
            c = self._geohash[i:i + 1]
            v = self._base_32_to_int(c)
            for mask in [2 ** j for j in reversed(range(0, 5))]:
                if is_even:
                    if v & mask:
                        lng = [sum(lng) / 2, lng[1]]
                    else:
                        lng = [lng[0], sum(lng) / 2]
                else:
                    if v & mask:
                        lat = [sum(lat) / 2, lat[1]]
                    else:
                        lat = [lat[0], sum(lat) / 2]
                is_even = not is_even

        return [lat, lng]

    def decode(self):
        [interval_lat, interval_lng] = self.decode_to_interval()

        places_lat = max(
            1, -(self._round(log10(interval_lat[1] - interval_lat[0])))) - 1
        places_lng = max(
            1, -(self._round(log10(interval_lng[1] - interval_lng[0])))) - 1

        lat = self._round(sum(interval_lat) / 2, places_lat)
        lng = self._round(sum(interval_lng) / 2, places_lng)

        return [lat, lng]

    def neighbors(self, order=1):
        if not isinstance(order, int) or order < 1:
            raise TypeError('"range" must be a natural number.')

        length = self.__len__()

        [interval_lat, interval_lng] = self.decode_to_interval()

        delta_lat = interval_lat[1] - interval_lat[0]
        delta_lng = interval_lng[1] - interval_lng[0]

        lat = sum(interval_lat) / 2
        lng = sum(interval_lng) / 2

        geohashes = []

        for i in range(-1 * order, order + 1):
            for j in range(-1 * order, order + 1):
                if i == 0 and j == 0:
                    continue

                lat_tmp = lat + delta_lat * i
                if lat_tmp < -90.0:
                    lat_tmp += 180.0
                elif lat_tmp > 90.0:
                    lat_tmp -= 180.0

                lng_tmp = lng + delta_lng * j
                if lng_tmp < -180.0:
                    lng_tmp += 360
                elif lng_tmp > 180.0:
                    lng_tmp -= 360.0

                geohashes.append(self._encode(lat_tmp, lng_tmp, length))

        return geohashes

    @staticmethod
    def _normalize_angle_180(lng):
        lng %= 360
        if lng <= 180:
            return lng
        else:
            return lng - 360

    def _normalize_lat(self, lat):
        lat = self._normalize_angle_180(lat)

        if lat >= 0:
            if lat > 90:
                return 180 - lat
        else:
            if lat < -90:
                return -180 - lat

        return lat

    @staticmethod
    def _bits_to_int(bits):
        return int(''.join(bits), 2)

    def _int_to_base_32(self, v):
        return self._BASE_32[v]

    def _base_32_to_int(self, c):
        return self._BASE_32.index(c)

    @staticmethod
    def _round(val, digit=0):
        p = 10 ** digit
        return (val * p * 2 + 1) // 2 / p
