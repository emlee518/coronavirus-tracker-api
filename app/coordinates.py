"""app.coordinates.py"""


class Coordinates:
    """
    A position on earth using decimal coordinates (latitude and longitude).
    """

    def __init__(self):
        self.lat_long = {}

class CBuilder():

    def build_latitude(self): pass
    def build_longitude(self): pass
    def get_result(self): pass

class Builder(CBuilder):

    def __init__(self):
        self.coordinates = Coordinates()

    def build_latitude(self, latitude):
        self.coordinates.lat_long["latitude"] = latitude
        return self

    def build_longitude(self, longitude):
        self.coordinates.lat_long["longitude"] = longitude
        return self

    def get_result(self):
        return self.coordinates.lat_long

class CDirector:
    lat: int
    long: int

    def construct(latitude, longitude):
        CDirector.lat = latitude
        CDirector.long = longitude

        return Builder()\
            .build_latitude(latitude)\
            .build_longitude(longitude)\
            .get_result()

    def serialize(self):
        """
        Serializes the coordinates into a dict.

        :returns: The serialized coordinates.
        :rtype: dict
        """
        return self

    def __str__(self):
        return "lat: %s, long: %s" % (CDirector.lat, CDirector.long)


