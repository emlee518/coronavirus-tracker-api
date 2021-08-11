"""app.location"""
from ..coordinates import Coordinates
from ..utils import countries
from ..utils.populations import country_population

class Leaf:  

    def __init__(self, value): 
        self.value = value
  
class Composite:
  
    def __init__(self, composite):
        self.composite = composite
        self.children = {}
  
    def add(self, key, value):
        self.children[key] = value
  
    def pop(self, key):
        self.children.pop(key)

# pylint: disable=redefined-builtin,invalid-name
class Location:  # pylint: disable=too-many-instance-attributes
    """
    A location in the world affected by the coronavirus.
    """

    root = Composite("root")
    latest = Composite("latest")
    def __init__(
        self, id, country, province, coordinates, last_updated, confirmed, deaths, recovered,
    ):  # pylint: disable=too-many-arguments
        # General info.
        self.root.add("id", Leaf(id).value)
        self.root.add("country", Leaf(country).value.strip())
        self.root.add("country_code", Leaf(self.country_code()).value)
        self.root.add("country_population", Leaf(self.country_population()).value)
        self.root.add("province", Leaf(province).value.strip())
        self.root.add("coordinates", Leaf(coordinates.serialize()).value)

        # Last update.
        self.root.add("last_updated", Leaf(last_updated).value)

        # Statistics.
        self.root.add("latest", self.latest.children)
        self.latest.add("confirmed", Leaf(confirmed).value)
        self.latest.add("deaths", Leaf(deaths).value)
        self.latest.add("recovered", Leaf(recovered).value)

    @property
    def country_code(self):
        """
        Gets the alpha-2 code represention of the country. Returns 'XX' if none is found.

        :returns: The country code.
        :rtype: str
        """
        return (countries.country_code(self.country) or countries.DEFAULT_COUNTRY_CODE).upper()

    @property
    def country_population(self):
        """
        Gets the population of this location.

        :returns: The population.
        :rtype: int
        """
        return country_population(self.country_code)

    def serialize(self):
        """
        Serializes the location into a dict.

        :returns: The serialized location.
        :rtype: dict
        """
        return self.root.children     


class TimelinedLocation(Location):
    """
    A location with timelines.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, id, country, province, coordinates, last_updated, timelines):
        super().__init__(
            # General info.
            id,
            country,
            province,
            coordinates,
            last_updated,
            # Statistics (retrieve latest from timelines).
            confirmed=timelines.get("confirmed").latest or 0,
            deaths=timelines.get("deaths").latest or 0,
            recovered=timelines.get("recovered").latest or 0,
        )

        # Set timelines.
        self.timelines = timelines

    # pylint: disable=arguments-differ
    def serialize(self, timelines=False):
        """
        Serializes the location into a dict.

        :param timelines: Whether to include the timelines.
        :returns: The serialized location.
        :rtype: dict
        """
        serialized = super().serialize()

        # Whether to include the timelines or not.
        if timelines:
            serialized.update(
                {
                    "timelines": {
                        # Serialize all the timelines.
                        key: value.serialize()
                        for (key, value) in self.timelines.items()
                    }
                }
            )

        # Return the serialized location.
        return serialized