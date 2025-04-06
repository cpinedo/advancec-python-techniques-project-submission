"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
import math

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, pdes, name, pha, diameter, **info):
        """Create a new `NearEarthObject`.

        :param pdes - the primary designation of the NEO. This is a unique identifier in the database, and its "name" to computer systems.
        :param name - the International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
        :param pha - whether NASA has marked the NEO as a "Potentially Hazardous Asteroid," roughly meaning that it's large and can come quite close to Earth.
        :param diameter - the NEO's diameter (from an equivalent sphere) in kilometers.
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = str(pdes) if pdes else None
        self.name = str(name) if name else None
        try:
            self.diameter = float(diameter)
        except (ValueError, TypeError):
            self.diameter = float('nan')

        self.hazardous = bool(pha == 'Y')

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.designation + ' ' + self.name

    def __str__(self):
        """Return `str(self)`."""
        return (f"NEO {self.designation} ({self.name or 'unnamed'}), "
                f"{'hazardous' if self.hazardous else 'non-hazardous'}, "
                f"diameter: {self.diameter if not math.isnan(self.diameter) else 'unknown'} km")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, des, cd, dist, v_rel, **info):
        """Create a new `CloseApproach`.

        :param des - primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
        :param cd - time of close-approach (formatted calendar date/time, in UTC)
        :param dist - nominal approach distance (au)
        :param v_rel - velocity relative to the approach body at close approach (km/s)
        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = str(des) if des else None
        self.time = cd_to_datetime(cd)

        try:
            self.distance = float(dist)
        except (ValueError, TypeError):
            self.distance = float('nan')

        try:
            self.velocity = float(v_rel)
        except (ValueError, TypeError):
            self.velocity = float('nan')

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        time_str = self.time_str

        if math.isnan(self.distance):
            dist_str = "an unknown distance"
        else:
            dist_str = f"{self.distance:.2f} au"

        if math.isnan(self.velocity):
            vel_str = "an unknown velocity"
        else:
            vel_str = f"{self.velocity:.2f} km/s"

        neo_reference = f"by {self.neo.name if self.neo and self.neo.name else self._designation}" \
            if self._designation else "by an unknown object"

        return (f"A CloseApproach at {time_str} {neo_reference}, "
                f"approaching at {dist_str} and a velocity of {vel_str}.")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"
