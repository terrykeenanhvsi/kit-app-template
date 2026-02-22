__all__ = ["PlanetLoader"]

from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List
import math
import csv
from pxr import Usd, Sdf
from omni.usd import get_context
import numpy as np
import random

@dataclass
class Ephemeris:
    """Ephemeris data structure for planet positions"""
    noon: datetime
    date: str
    sun: str
    venus: str
    mercury: str
    moon: str
    mars: str
    jupiter: str
    saturn: str
    uranus: str
    neptune: str
    pluto: str


@dataclass
class NatalPlanetStruct:
    """Natal planet structure"""
    noon: datetime = None
    name: str = ""
    degree: float = 0.0
    sign: int = 0
    house: int = 0
    position: tuple = (0, 0, 0)  # x, y, z


@dataclass
class CurrentPlanetStruct:
    """Current planet structure"""
    noon: datetime = None
    name: str = ""
    degree: float = 0.0
    sign: int = 0
    house: int = 0
    position: tuple = (0, 0, 0)  # x, y, z


@dataclass
class ChakraStruct:
    """Chakra structure"""
    name: str = ""
    total_good: float = 0.0
    total_bad: float = 0.0
    total_sextile: float = 0.0
    total_square: float = 0.0
    total_trine: float = 0.0
    total_opposite: float = 0.0
    total_conjunct: float = 0.0
    total_aspect: float = 0.0

    natal_good: float = 0.0
    natal_bad: float = 0.0
    natal_sextile: float = 0.0
    natal_square: float = 0.0
    natal_trine: float = 0.0
    natal_opposite: float = 0.0
    natal_conjunct: float = 0.0
    natal_total: float = 0.0

    current_good: float = 0.0
    current_bad: float = 0.0
    current_sextile: float = 0.0
    current_square: float = 0.0
    current_trine: float = 0.0
    current_opposite: float = 0.0
    current_conjunct: float = 0.0
    current_total: float = 0.0


@dataclass
class PlanetAspectsStruct:
    """Planet aspects structure"""
    sun_diff: float = 0.0
    moon_diff: float = 0.0
    mercury_diff: float = 0.0
    venus_diff: float = 0.0
    mars_diff: float = 0.0
    jupiter_diff: float = 0.0
    saturn_diff: float = 0.0
    uranus_diff: float = 0.0
    neptune_diff: float = 0.0
    pluto_diff: float = 0.0
    marker_diff: float = 0.0

    sun_diff_cur: float = 0.0
    moon_diff_cur: float = 0.0
    mercury_diff_cur: float = 0.0
    venus_diff_cur: float = 0.0
    mars_diff_cur: float = 0.0
    jupiter_diff_cur: float = 0.0
    saturn_diff_cur: float = 0.0
    uranus_diff_cur: float = 0.0
    neptune_diff_cur: float = 0.0
    pluto_diff_cur: float = 0.0
    marker_diff_cur: float = 0.0

@dataclass
class ChakraTargetStruct:
    """Chakra target structure"""
    name: str = ""
    target: float = 0.0
    weight: float = 0.0
    aspect_type: int = 5  # 0=conjunct, 1=sextile, 2=square, 3=trine, 4=opposite
    total_good: float = 0.0
    total_bad: float = 0.0
    total_sextile: float = 0.0
    total_square: float = 0.0
    total_trine: float = 0.0
    total_opposite: float = 0.0
    total_conjunct: float = 0.0
    total_aspect: float = 0.0

@dataclass
class PlanetWeightsStruct:
    """Planet weights structure"""
    sun_weight: float = 0.0
    sun_aspect_type: int = 5  # 0=conjunct, 1=sextile, 2=square, 3=trine, 4=opposite
    moon_weight: float = 0.0
    moon_aspect_type: int = 5
    mercury_weight: float = 0.0
    mercury_aspect_type: int = 5
    venus_weight: float = 0.0
    venus_aspect_type: int = 5
    mars_weight: float = 0.0
    mars_aspect_type: int = 5
    jupiter_weight: float = 0.0
    jupiter_aspect_type: int = 5
    saturn_weight: float = 0.0
    saturn_aspect_type: int = 5
    uranus_weight: float = 0.0
    uranus_aspect_type: int = 5
    neptune_weight: float = 0.0
    neptune_aspect_type: int = 5
    pluto_weight: float = 0.0
    pluto_aspect_type: int = 5
    marker_weight: float = 0.0
    marker_aspect_type: int = 5

    total_good: float = 0.0
    total_bad: float = 0.0
    total_sextile: float = 0.0
    total_square: float = 0.0
    total_trine: float = 0.0
    total_opposite: float = 0.0
    total_conjunct: float = 0.0
    total_aspect: float = 0.0

    marker_good: float = 0.0
    marker_bad: float = 0.0
    marker_sextile: float = 0.0
    marker_square: float = 0.0
    marker_trine: float = 0.0
    marker_opposite: float = 0.0
    marker_conjunct: float = 0.0
    marker_aspect: float = 0.0


class PlanetLoader:
    """Main PlanetLoader class for processing astrological planet data"""

    def __init__(self):
        """Initialize PlanetLoader with default values"""
        # Class variables
        self.chakra_list: List[ChakraStruct] = []
        self.natal_weight_list: List[PlanetWeightsStruct] = []
        self.current_weight_list: List[PlanetWeightsStruct] = []
        self.planet_aspects: List[PlanetAspectsStruct] = []
        self.planets: List[Ephemeris] = []
        self.natal_planets: List[NatalPlanetStruct] = []
        self.current_planets_2: List[CurrentPlanetStruct] = []

        self.sun: ChakraTargetStruct = ChakraTargetStruct()
        self.moon: ChakraTargetStruct = ChakraTargetStruct()
        self.mercury: ChakraTargetStruct = ChakraTargetStruct()
        self.venus: ChakraTargetStruct = ChakraTargetStruct()
        self.mars: ChakraTargetStruct = ChakraTargetStruct()
        self.jupiter: ChakraTargetStruct = ChakraTargetStruct()
        self.saturn: ChakraTargetStruct = ChakraTargetStruct()
        self.uranus: ChakraTargetStruct = ChakraTargetStruct()
        self.neptune: ChakraTargetStruct = ChakraTargetStruct()
        self.pluto: ChakraTargetStruct = ChakraTargetStruct()
        self.marker: ChakraTargetStruct = ChakraTargetStruct()

        self.sun_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.moon_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.mercury_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.venus_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.mars_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.jupiter_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.saturn_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.uranus_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.neptune_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.pluto_cur: ChakraTargetStruct = ChakraTargetStruct()
        self.marker_cur: ChakraTargetStruct = ChakraTargetStruct()

        # self.King_Wands_cur: ChakraTargetStruct
        # self.Queen_Wands_cur: ChakraTargetStruct
        # self.Knight_Wands_cur: ChakraTargetStruct
        # self.Ace_Wands_cur: ChakraTargetStruct
        # self.Two_Wands_cur: ChakraTargetStruct
        # self.Three_Wands_cur: ChakraTargetStruct
        # self.Four_Wands_cur: ChakraTargetStruct
        # self.Five_Wands_cur: ChakraTargetStruct
        # self.Six_Wands_cur: ChakraTargetStruct
        # self.Seven_Wands_cur: ChakraTargetStruct
        # self.Eight_Wands_cur: ChakraTargetStruct
        # self.Nine_Wands_cur: ChakraTargetStruct
        # self.Ten_Wands_cur: ChakraTargetStruct

        # self.King_Cups_cur: ChakraTargetStruct
        # self.Queen_Cups_cur: ChakraTargetStruct
        # self.Knight_Cups_cur: ChakraTargetStruct
        # self.Ace_Cups_cur: ChakraTargetStruct
        # self.Two_Cups_cur: ChakraTargetStruct
        # self.Three_Cups_cur: ChakraTargetStruct
        # self.Four_Cups_cur: ChakraTargetStruct
        # self.Five_Cups_cur: ChakraTargetStruct
        # self.Six_Cups_cur: ChakraTargetStruct
        # self.Seven_Cups_cur: ChakraTargetStruct
        # self.Eight_Cups_cur: ChakraTargetStruct
        # self.Nine_Cups_cur: ChakraTargetStruct
        # self.Ten_Cups_cur: ChakraTargetStruct

        # self.King_Swords_cur: ChakraTargetStruct
        # self.Queen_Swords_cur: ChakraTargetStruct
        # self.Knight_Swords_cur: ChakraTargetStruct
        # self.Ace_Swords_cur: ChakraTargetStruct
        # self.Two_Swords_cur: ChakraTargetStruct
        # self.Three_Swords_cur: ChakraTargetStruct
        # self.Four_Swords_cur: ChakraTargetStruct
        # self.Five_Swords_cur: ChakraTargetStruct
        # self.Six_Swords_cur: ChakraTargetStruct
        # self.Seven_Swords_cur: ChakraTargetStruct
        # self.Eight_Swords_cur: ChakraTargetStruct
        # self.Nine_Swords_cur: ChakraTargetStruct
        # self.Ten_Swords_cur: ChakraTargetStruct

        # self.King_Pentacles_cur: ChakraTargetStruct
        # self.Queen_Pentacles_cur: ChakraTargetStruct
        # self.Knight_Pentacles_cur: ChakraTargetStruct
        # self.Ace_Pentacles_cur: ChakraTargetStruct
        # self.Two_Pentacles_cur: ChakraTargetStruct
        # self.Three_Pentacles_cur: ChakraTargetStruct
        # self.Four_Pentacles_cur: ChakraTargetStruct
        # self.Five_Pentacles_cur: ChakraTargetStruct
        # self.Six_Pentacles_cur: ChakraTargetStruct
        # self.Seven_Pentacles_cur: ChakraTargetStruct
        # self.Eight_Pentacles_cur: ChakraTargetStruct
        # self.Nine_Pentacles_cur: ChakraTargetStruct
        # self.Ten_Pentacles_cur: ChakraTargetStruct

        # Planet difference values
        self.sun_diff = 0.0
        self.moon_diff = 0.0
        self.mercury_diff = 0.0
        self.venus_diff = 0.0
        self.mars_diff = 0.0
        self.jupiter_diff = 0.0
        self.saturn_diff = 0.0
        self.uranus_diff = 0.0
        self.neptune_diff = 0.0
        self.pluto_diff = 0.0
        self.marker_diff = 0.0

        # Game Objects (None in Python, would be UI references)
        # self.sun_cur = None
        # self.moon_cur = None
        # self.venus_cur = None
        # self.mercury_cur = None
        # self.mars_cur = None
        # self.jupiter_cur = None
        # self.saturn_cur = None
        # self.uranus_cur = None
        # self.neptune = None
        # self.pluto = None

        # Planet arrays
        self.terry_planets_float: List[float] = []
        self.terry_planets: List[str] = []
        self.terry_planets_entries: List[str] = []
        self.terry_planet_signs: List[int] = []
        self.current_planets: List[str] = []
        self.current_planets_entries: List[str] = []
        self.current_planet_signs: List[int] = []
        self.noon_planets: List[str] = []
        self.noon_planet_signs: List[int] = []
        self.right_tomorrow_planets: List[str] = []
        self.right_tomorrow_planet_signs: List[int] = []
        self.right_yesterday_planets: List[str] = []
        self.right_yesterday_planet_signs: List[int] = []
        self.left_noon_planets: List[str] = []
        self.left_noon_planet_signs: List[int] = []
        self.left_tomorrow_planets: List[str] = []
        self.left_tomorrow_planet_signs: List[int] = []
        self.left_yesterday_planets: List[str] = []
        self.left_yesterday_planet_signs: List[int] = []
        self.right_noon_planets: List[str] = []
        self.right_noon_planet_signs: List[int] = []

        # Date/Time variables
        self.last = datetime.now()
        self.noon = datetime.now()
        self.today = datetime.now()
        self.terry = datetime(1959, 2, 28)
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.yesterday = datetime.now() - timedelta(days=1)
        self.natal_chart = datetime(2000, 2, 28)
        self.default = datetime(1959, 2, 28)
        self.left_side_display = datetime.now()
        self.right_side_display = datetime.now()
        self.left_time_display = 0.0
        self.right_time_display = 0.0
        self.left_marker_display = 0.0
        self.right_marker_display = 0.0

        # Other variables
        self.reader = None
        self.line = ""
        self.frame_count = 0
        self.ephemeris_txt = None
        self.planet_differences = PlanetAspectsStruct()
        self.planet_weights = PlanetWeightsStruct()
        self.chakra = ChakraStruct()
        self.complete = "Not Started"
        self.csvFile = None
        self.rows = None
        self.range = 10

    def start(self, sliderLeftValue: int, sliderRightValue: int):
        """Initialize the PlanetLoader (called on startup)"""
        # Load ephemeris data

        self.sun.name = "Sun"
        self.sun.aspect_type = 5
        self.sun.weight = 0.0
        self.sun.total_aspect = 0.0
        self.sun.total_good = 0.0
        self.sun.total_bad = 0.0
        self.sun.total_conjunct = 0.0
        self.sun.total_sextile = 0.0
        self.sun.total_square = 0.0
        self.sun.total_trine = 0.0
        self.sun.total_opposite = 0.0

        self.moon.name = "Moon"
        self.moon.aspect_type = 5
        self.moon.weight = 0.0
        self.moon.total_aspect = 0.0
        self.moon.total_good = 0.0
        self.moon.total_bad = 0.0
        self.moon.total_conjunct = 0.0
        self.moon.total_sextile = 0.0
        self.moon.total_square = 0.0
        self.moon.total_trine = 0.0
        self.moon.total_opposite = 0.0

        self.mercury.name = "Mercury"
        self.mercury.aspect_type = 5
        self.mercury.weight = 0.0
        self.mercury.total_aspect = 0.0
        self.mercury.total_good = 0.0
        self.mercury.total_bad = 0.0
        self.mercury.total_conjunct = 0.0
        self.mercury.total_sextile = 0.0
        self.mercury.total_square = 0.0
        self.mercury.total_trine = 0.0
        self.mercury.total_opposite = 0.0

        self.venus.name = "Venus"
        self.venus.aspect_type = 5
        self.venus.weight = 0.0
        self.venus.total_aspect = 0.0
        self.venus.total_good = 0.0
        self.venus.total_bad = 0.0
        self.venus.total_conjunct = 0.0
        self.venus.total_sextile = 0.0
        self.venus.total_square = 0.0
        self.venus.total_trine = 0.0
        self.venus.total_opposite = 0.0

        self.mars.name = "Mars"
        self.mars.aspect_type = 5
        self.mars.weight = 0.0
        self.mars.total_aspect = 0.0
        self.mars.total_good = 0.0
        self.mars.total_bad = 0.0
        self.mars.total_conjunct = 0.0
        self.mars.total_sextile = 0.0
        self.mars.total_square = 0.0
        self.mars.total_trine = 0.0
        self.mars.total_opposite = 0.0

        self.jupiter.name = "Jupiter"
        self.jupiter.aspect_type = 5
        self.jupiter.weight = 0.0
        self.jupiter.total_aspect = 0.0
        self.jupiter.total_good = 0.0
        self.jupiter.total_bad = 0.0
        self.jupiter.total_conjunct = 0.0
        self.jupiter.total_sextile = 0.0
        self.jupiter.total_square = 0.0
        self.jupiter.total_trine = 0.0
        self.jupiter.total_opposite = 0.0

        self.saturn.name = "Saturn"
        self.saturn.aspect_type = 5
        self.saturn.weight = 0.0
        self.saturn.total_aspect = 0.0
        self.saturn.total_good = 0.0
        self.saturn.total_bad = 0.0
        self.saturn.total_conjunct = 0.0
        self.saturn.total_sextile = 0.0
        self.saturn.total_square = 0.0
        self.saturn.total_trine = 0.0
        self.saturn.total_opposite = 0.0

        self.uranus.name = "Uranus"
        self.uranus.aspect_type = 5
        self.uranus.weight = 0.0
        self.uranus.total_aspect = 0.0
        self.uranus.total_good = 0.0
        self.uranus.total_bad = 0.0
        self.uranus.total_conjunct = 0.0
        self.uranus.total_sextile = 0.0
        self.uranus.total_square = 0.0
        self.uranus.total_trine = 0.0
        self.uranus.total_opposite = 0.0

        self.neptune.name = "Neptune"
        self.neptune.aspect_type = 5
        self.neptune.weight = 0.0
        self.neptune.total_aspect = 0.0
        self.neptune.total_good = 0.0
        self.neptune.total_bad = 0.0
        self.neptune.total_conjunct = 0.0
        self.neptune.total_sextile = 0.0
        self.neptune.total_square = 0.0
        self.neptune.total_trine = 0.0
        self.neptune.total_opposite = 0.0

        self.pluto.name = "Pluto"
        self.pluto.aspect_type = 5
        self.pluto.weight = 0.0
        self.pluto.total_aspect = 0.0
        self.pluto.total_good = 0.0
        self.pluto.total_bad = 0.0
        self.pluto.total_conjunct = 0.0
        self.pluto.total_sextile = 0.0
        self.pluto.total_square = 0.0
        self.pluto.total_trine = 0.0
        self.pluto.total_opposite = 0.0

        self.marker.name = "marker"
        self.marker.aspect_type = 5
        self.marker.weight = 0.0
        self.marker.total_aspect = 0.0
        self.marker.total_good = 0.0
        self.marker.total_bad = 0.0
        self.marker.total_conjunct = 0.0
        self.marker.total_sextile = 0.0
        self.marker.total_square = 0.0
        self.marker.total_trine = 0.0
        self.marker.total_opposite = 0.0

        self.sun_cur.name = "Sun Current"
        self.sun_cur.aspect_type = 5
        self.sun_cur.weight = 0.0
        self.sun_cur.total_aspect = 0.0
        self.sun_cur.total_good = 0.0
        self.sun_cur.total_bad = 0.0
        self.sun_cur.total_sextile = 0.0
        self.sun_cur.total_conjunct = 0.0
        self.sun_cur.total_square = 0.0
        self.sun_cur.total_trine = 0.0
        self.sun_cur.total_opposite = 0.0

        self.mercury_cur.name = "Mercury Current"
        self.mercury_cur.aspect_type = 5
        self.mercury_cur.weight = 0.0
        self.mercury_cur.total_aspect = 0.0
        self.mercury_cur.total_good = 0.0
        self.mercury_cur.total_bad = 0.0
        self.mercury_cur.total_sextile = 0.0
        self.mercury_cur.total_conjunct = 0.0
        self.mercury_cur.total_square = 0.0
        self.mercury_cur.total_trine = 0.0
        self.mercury_cur.total_opposite = 0.0

        self.venus_cur.name = "Venus Current"
        self.venus_cur.aspect_type = 5
        self.venus_cur.weight = 0.0
        self.venus_cur.total_aspect = 0.0
        self.venus_cur.total_good = 0.0
        self.venus_cur.total_bad = 0.0
        self.venus_cur.total_sextile = 0.0
        self.venus_cur.total_conjunct = 0.0
        self.venus_cur.total_square = 0.0
        self.venus_cur.total_trine = 0.0
        self.venus_cur.total_opposite = 0.0

        self.moon_cur.name = "Moon Current"
        self.moon_cur.aspect_type = 5
        self.moon_cur.weight = 0.0
        self.moon_cur.total_aspect = 0.0
        self.moon_cur.total_good = 0.0
        self.moon_cur.total_bad = 0.0
        self.moon_cur.total_conjunct = 0.0
        self.moon_cur.total_sextile = 0.0
        self.moon_cur.total_square = 0.0
        self.moon_cur.total_trine = 0.0
        self.moon_cur.total_opposite = 0.0

        self.mars_cur.name = "Mars Current"
        self.mars_cur.aspect_type = 5
        self.mars_cur.weight = 0.0
        self.mars_cur.total_aspect = 0.0
        self.mars_cur.total_good = 0.0
        self.mars_cur.total_bad = 0.0
        self.mars_cur.total_sextile = 0.0
        self.mars_cur.total_conjunct = 0.0
        self.mars_cur.total_square = 0.0
        self.mars_cur.total_trine = 0.0
        self.mars_cur.total_opposite = 0.0

        self.jupiter_cur.name = "Jupiter Current"
        self.jupiter_cur.aspect_type = 5
        self.jupiter_cur.weight = 0.0
        self.jupiter_cur.total_aspect = 0.0
        self.jupiter_cur.total_good = 0.0
        self.jupiter_cur.total_bad = 0.0
        self.jupiter_cur.total_sextile = 0.0
        self.jupiter_cur.total_conjunct = 0.0
        self.jupiter_cur.total_square = 0.0
        self.jupiter_cur.total_trine = 0.0
        self.jupiter_cur.total_opposite = 0.0

        self.saturn_cur.name = "Saturn Current"
        self.saturn_cur.aspect_type = 5
        self.saturn_cur.weight = 0.0
        self.saturn_cur.total_aspect = 0.0
        self.saturn_cur.total_good = 0.0
        self.saturn_cur.total_bad = 0.0
        self.saturn_cur.total_sextile = 0.0
        self.saturn_cur.total_conjunct = 0.0
        self.saturn_cur.total_square = 0.0
        self.saturn_cur.total_trine = 0.0
        self.saturn_cur.total_opposite = 0.0

        self.uranus_cur.name = "Uranus Current"
        self.uranus_cur.aspect_type = 5
        self.uranus_cur.weight = 0.0
        self.uranus_cur.total_aspect = 0.0
        self.uranus_cur.total_good = 0.0
        self.uranus_cur.total_bad = 0.0
        self.uranus_cur.total_sextile = 0.0
        self.uranus_cur.total_conjunct = 0.0
        self.uranus_cur.total_square = 0.0
        self.uranus_cur.total_trine = 0.0
        self.uranus_cur.total_opposite = 0.0

        self.neptune_cur.name = "Neptune Current"
        self.neptune_cur.aspect_type = 5
        self.neptune_cur.weight = 0.0
        self.neptune_cur.total_aspect = 0.0
        self.neptune_cur.total_good = 0.0
        self.neptune_cur.total_bad = 0.0
        self.neptune_cur.total_sextile = 0.0
        self.neptune_cur.total_conjunct = 0.0
        self.neptune_cur.total_square = 0.0
        self.neptune_cur.total_trine = 0.0
        self.neptune_cur.total_opposite = 0.0

        self.pluto_cur.name = "Pluto Current"
        self.pluto_cur.aspect_type = 5
        self.pluto_cur.weight = 0.0
        self.pluto_cur.total_aspect = 0.0
        self.pluto_cur.total_good = 0.0
        self.pluto_cur.total_bad = 0.0
        self.pluto_cur.total_sextile = 0.0
        self.pluto_cur.total_conjunct = 0.0
        self.pluto_cur.total_square = 0.0
        self.pluto_cur.total_trine = 0.0
        self.pluto_cur.total_opposite = 0.0

        self.marker_cur.name = "marker Current"
        self.marker_cur.aspect_type = 5
        self.marker_cur.weight = 0.0
        self.marker_cur.total_aspect = 0.0
        self.marker_cur.total_good = 0.0
        self.marker_cur.total_bad = 0.0
        self.marker_cur.total_sextile = 0.0
        self.marker_cur.total_conjunct = 0.0
        self.marker_cur.total_square = 0.0
        self.marker_cur.total_trine = 0.0
        self.marker_cur.total_opposite = 0.0

        self.load_ephemeris_data()

        # for t in range(length):
        #     if t > 1:
        #         whole = self.rows[t]
        #         dateNoon = self.rows[t][0]
        #         newEntries = whole.split(',')
        #         newEntries_date = dateNoon.split('/')


        # Initialize dates
        # formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        self.last = datetime(2010, 1, 2)
        self.noon = datetime(2010, 1, 2)
        self.today = datetime.now()
        # self.today = self.today.strftime("%Y-%m-%d")
        self.terry = datetime(1959, 2, 28)
        self.tomorrow = datetime.now() + timedelta(days=1)
        # self.tomorrow = self.tomorrow.strftime("%Y-%m-%d")
        self.yesterday = datetime.now() - timedelta(days=1)
        # self.yesterday = self.yesterday.strftime("%Y-%m-%d")
        self.natal_chart = datetime(2000, 2, 28)
        self.default = datetime(1959, 2, 28)

        # Calculate current time
        hour = self.today.hour
        minute = self.today.minute
        second = self.today.second
        time = hour + (minute / 60) + (second / (60 * 60))
        print("Calling self Load:")
        self.load(self.default, 8.667, self.today, time, sliderLeftValue, sliderRightValue)

    def load_ephemeris_data(self) -> str:
        """Load ephemeris data from file or resource"""
        print("Load ephemeris data from file or resource")

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Ephemeris.csv', mode='r') as file:
            self.ephemeris_txt = csv.reader(file)
            self.rows = list(self.ephemeris_txt)
            print("Ephemirs 5-2 = ", self.rows[5][2])
            print("self.noon = ", self.noon)
            # print("Read File again < 1: ",self.rows[5][0])
            #for lines in csvFile:
            #   print(lines)

    def load(self, left_side: datetime, left_time: float, right_side: datetime,
             right_time: float, marker_left: float, marker_right: float):
        """Main load function for planet data"""

        print("Start loading:")

        self.complete = "Calculating"

        self.left_side_display = left_side
        self.right_side_display = right_side
        self.left_time_display = left_time
        self.right_time_display = right_time
        self.left_marker_display = marker_left
        self.right_marker_display = marker_right

        if not self.ephemeris_txt:
            print("self.ephemeris_txt return:")
            return

        # Clear lists
        self.natal_planets.clear()
        self.current_planets_2.clear()
        self.natal_weight_list.clear()
        self.current_weight_list.clear()
        self.planet_aspects.clear()

        self.frame_count = 0
        self.natal_chart = left_side

        # Parse ephemeris data
        # lines = self.ephemeris_txt.split('\n')


        self.rows[5][2]
        length = len(self.rows)
        t = 1
        for i in range(1,length - 1):
            entries = self.rows[i]
            # print("Find Data :", i, " Date: ", self.rows[i][0])
            # if(i == 54423):
            #     print("Here it is 54423")

            dateNoon = self.rows[i][0]
            dateNoon_formatted = dateNoon.split('/')
            # print("dateNoon_formatted:", dateNoon_formatted)
            self.month = dateNoon_formatted[0]
            self.day = dateNoon_formatted[1]
            self.year = dateNoon_formatted[2]

            if(len(self.month) < 2):
                self.month = "0" + self.month
            if(len(self.day) < 2):
                self.day = "0" + self.day
            if(i < 36162):
                self.year = "19" + self.year
            else:
                self.year = "20" + self.year

            # # dateNoon_formatted_date = month + "/" + day + "/" + year
            self.noon = datetime(int(self.year), int(self.month), int(self.day))
            # print("self.noon", self.noon)
            # print("month :", self.month, "day :", self.day, "year :", self.year)

            # Check for matching dates
            if self.noon.date() == right_side.date():
                self.noon_planets = entries
                self.current_planets_entries = entries
                self.current_planets = entries[:11] + [str(marker_right), str(marker_left)]
                print("Found it", i)

            if self.noon.date() == (right_side + timedelta(days=1)).date():
                self.right_tomorrow_planets = entries
                print("self.right_tomorrow_planets = ", self.right_tomorrow_planets)

            if self.noon.date() == (right_side - timedelta(days=1)).date():
                self.right_yesterday_planets = entries
                print("self.right_yesterday_planets = ", self.right_yesterday_planets)

            if self.noon.date() == self.natal_chart.date():
                self.terry_planets_entries = entries
                self.terry_planets = entries[:11] + [str(marker_left), str(marker_right)]
                print("self.terry_planets = ", self.terry_planets)

            # if self.noon.date() == left_side.date():
                self.left_noon_planets = entries
                print("self.left_noon_planets = ", self.left_noon_planets)

            if self.noon.date() == (left_side + timedelta(days=1)).date():
                self.left_tomorrow_planets = entries
                print("self.left_tomorrow_planets = ", self.left_tomorrow_planets)

            if self.noon.date() == (left_side - timedelta(days=1)).date():
                self.left_yesterday_planets = entries
                print("self.left_yesterday_planets = ", self.left_yesterday_planets)

         # Process right side planet corrections
        if right_time > 12:
            right_corrected_time = (right_time - 12) / 24
            self._calculate_planet_diffs_tomorrow(self.right_tomorrow_planets, self.noon_planets)
        else:
            right_corrected_time = (right_time + 12) / 24
            self._calculate_planet_diffs_yesterday(self.noon_planets, self.right_yesterday_planets)

        self._apply_time_correction(right_corrected_time)
        self._update_current_planets(right_time)

        # Process left side planet corrections
        if left_time > 12:
            left_corrected_time = (left_time - 12) / 24
            self._calculate_planet_diffs_tomorrow(self.left_tomorrow_planets, self.left_noon_planets)
        else:
            left_corrected_time = (left_time + 12) / 24
            self._calculate_planet_diffs_yesterday(self.left_noon_planets, self.left_yesterday_planets)

        self._apply_time_correction(left_corrected_time)
        self._update_terry_planets(left_time)

        # Calculate aspects
        self._calculate_aspects(marker_left, marker_right)

        # Calculate weights
        self._calculate_weights()

        # Create planet information
        self._create_planet_info()

        # Create chakra list
        self._create_chakra_list()

        # Save chakra data to file
        self.save_file_chakras()

        self.complete = "Load Complete"
        print("Returning done = ")

        # for k in range(11):
        #     print("Planet ", k, " Current: ", self.current_planets[k], " Natal: ", self.terry_planets[k])

        # for k in range(11):
        #    print("Natal Weights List ", k, " : ", self.natal_weight_list[k])

        # for k in range(11):
        #    print("Current Weights List ", k, " : ", self.current_weight_list[k])

        # for k in range(10):
        #     print("Natal Planet ", k, " : ", self.natal_planets[k])

        # for k in range(10):
        #     print("Terry Planet Signs ", k, " : ", self.terry_planet_signs[k])

        # for k in range(10):
        #     print("Current Planet ", k, " : ", self.current_planets_2[k])

        # for k in range(10):
        #     print("Current Planet Signs ", k, " : ", self.current_planet_signs[k])

    def _calculate_planet_diffs_tomorrow(self, tomorrow_planets, noon_planets):
        """Calculate planet differences for tomorrow"""
        self.sun_diff = float(tomorrow_planets[1]) - float(noon_planets[1])
        self.moon_diff = float(tomorrow_planets[2]) - float(noon_planets[2])
        self.mercury_diff = float(tomorrow_planets[3]) - float(noon_planets[3])
        self.venus_diff = float(tomorrow_planets[4]) - float(noon_planets[4])
        self.mars_diff = float(tomorrow_planets[5]) - float(noon_planets[5])
        self.jupiter_diff = float(tomorrow_planets[6]) - float(noon_planets[6])
        self.saturn_diff = float(tomorrow_planets[7]) - float(noon_planets[7])
        self.uranus_diff = float(tomorrow_planets[8]) - float(noon_planets[8])
        self.neptune_diff = float(tomorrow_planets[9]) - float(noon_planets[9])
        self.pluto_diff = float(tomorrow_planets[10]) - float(noon_planets[10])

    def _calculate_planet_diffs_yesterday(self, noon_planets, yesterday_planets):
        """Calculate planet differences for yesterday"""
        self.sun_diff = float(noon_planets[1]) - float(yesterday_planets[1])
        self.moon_diff = float(noon_planets[2]) - float(yesterday_planets[2])
        self.mercury_diff = float(noon_planets[3]) - float(yesterday_planets[3])
        self.venus_diff = float(noon_planets[4]) - float(yesterday_planets[4])
        self.mars_diff = float(noon_planets[5]) - float(yesterday_planets[5])
        self.jupiter_diff = float(noon_planets[6]) - float(yesterday_planets[6])
        self.saturn_diff = float(noon_planets[7]) - float(yesterday_planets[7])
        self.uranus_diff = float(noon_planets[8]) - float(yesterday_planets[8])
        self.neptune_diff = float(noon_planets[9]) - float(yesterday_planets[9])
        self.pluto_diff = float(noon_planets[10]) - float(yesterday_planets[10])

    def _apply_time_correction(self, corrected_time: float):
        """Apply time correction to planet differences"""
        self.sun_diff *= corrected_time
        self.moon_diff *= corrected_time
        self.mercury_diff *= corrected_time
        self.venus_diff *= corrected_time
        self.mars_diff *= corrected_time
        self.jupiter_diff *= corrected_time
        self.saturn_diff *= corrected_time
        self.uranus_diff *= corrected_time
        self.neptune_diff *= corrected_time
        self.pluto_diff *= corrected_time

    def _update_current_planets(self, right_time: float):
        """Update current planets with corrected values"""
        if right_time > 12:
            self.current_planets[1] = str(float(self.noon_planets[1]) + self.sun_diff)
            self.current_planets[2] = str(float(self.noon_planets[2]) + self.moon_diff)
            self.current_planets[3] = str(float(self.noon_planets[3]) + self.mercury_diff)
            self.current_planets[4] = str(float(self.noon_planets[4]) + self.venus_diff)
            self.current_planets[5] = str(float(self.noon_planets[5]) + self.mars_diff)
            self.current_planets[6] = str(float(self.noon_planets[6]) + self.jupiter_diff)
            self.current_planets[7] = str(float(self.noon_planets[7]) + self.saturn_diff)
            self.current_planets[8] = str(float(self.noon_planets[8]) + self.uranus_diff)
            self.current_planets[9] = str(float(self.noon_planets[9]) + self.neptune_diff)
            self.current_planets[10] = str(float(self.noon_planets[10]) + self.pluto_diff)
        else:
            self.current_planets[1] = str(float(self.right_yesterday_planets[1]) + self.sun_diff)
            self.current_planets[2] = str(float(self.right_yesterday_planets[2]) + self.moon_diff)
            self.current_planets[3] = str(float(self.right_yesterday_planets[3]) + self.mercury_diff)
            self.current_planets[4] = str(float(self.right_yesterday_planets[4]) + self.venus_diff)
            self.current_planets[5] = str(float(self.right_yesterday_planets[5]) + self.mars_diff)
            self.current_planets[6] = str(float(self.right_yesterday_planets[6]) + self.jupiter_diff)
            self.current_planets[7] = str(float(self.right_yesterday_planets[7]) + self.saturn_diff)
            self.current_planets[8] = str(float(self.right_yesterday_planets[8]) + self.uranus_diff)
            self.current_planets[9] = str(float(self.right_yesterday_planets[9]) + self.neptune_diff)
            self.current_planets[10] = str(float(self.right_yesterday_planets[10]) + self.pluto_diff)

    def _update_terry_planets(self, left_time: float):
        """Update Terry (natal) planets with corrected values"""
        if left_time > 12:
            self.terry_planets[1] = str(float(self.left_noon_planets[1]) + self.sun_diff)
            self.terry_planets[2] = str(float(self.left_noon_planets[2]) + self.moon_diff)
            self.terry_planets[3] = str(float(self.left_noon_planets[3]) + self.mercury_diff)
            self.terry_planets[4] = str(float(self.left_noon_planets[4]) + self.venus_diff)
            self.terry_planets[5] = str(float(self.left_noon_planets[5]) + self.mars_diff)
            self.terry_planets[6] = str(float(self.left_noon_planets[6]) + self.jupiter_diff)
            self.terry_planets[7] = str(float(self.left_noon_planets[7]) + self.saturn_diff)
            self.terry_planets[8] = str(float(self.left_noon_planets[8]) + self.uranus_diff)
            self.terry_planets[9] = str(float(self.left_noon_planets[9]) + self.neptune_diff)
            self.terry_planets[10] = str(float(self.left_noon_planets[10]) + self.pluto_diff)
        else:
            self.terry_planets[1] = str(float(self.left_yesterday_planets[1]) + self.sun_diff)
            self.terry_planets[2] = str(float(self.left_yesterday_planets[2]) + self.moon_diff)
            self.terry_planets[3] = str(float(self.left_yesterday_planets[3]) + self.mercury_diff)
            self.terry_planets[4] = str(float(self.left_yesterday_planets[4]) + self.venus_diff)
            self.terry_planets[5] = str(float(self.left_yesterday_planets[5]) + self.mars_diff)
            self.terry_planets[6] = str(float(self.left_yesterday_planets[6]) + self.jupiter_diff)
            self.terry_planets[7] = str(float(self.left_yesterday_planets[7]) + self.saturn_diff)
            self.terry_planets[8] = str(float(self.left_yesterday_planets[8]) + self.uranus_diff)
            self.terry_planets[9] = str(float(self.left_yesterday_planets[9]) + self.neptune_diff)
            self.terry_planets[10] = str(float(self.left_yesterday_planets[10]) + self.pluto_diff)

    def _calculate_aspects(self, marker_left: float, marker_right: float):
        """Calculate aspects between natal and current planets"""
        for j in range(1, 12):
            planet_diff = PlanetAspectsStruct()

            # Calculate differences between planets
            planet_diff.sun_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[1]))
            if planet_diff.sun_diff > 180:
                planet_diff.sun_diff = abs(abs(planet_diff.sun_diff) - 360)

            planet_diff.moon_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[2]))
            if planet_diff.moon_diff > 180:
                planet_diff.moon_diff = abs(abs(planet_diff.moon_diff) - 360)

            planet_diff.mercury_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[3]));
            if planet_diff.mercury_diff > 180:
                planet_diff.mercury_diff = abs(abs(planet_diff.mercury_diff) - 360)

            planet_diff.venus_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[4]))
            if planet_diff.venus_diff > 180:
                planet_diff.venus_diff = abs(abs(planet_diff.venus_diff) - 360)

            planet_diff.mars_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[5]))
            if planet_diff.mars_diff > 180:
                planet_diff.mars_diff = abs(abs(planet_diff.mars_diff) - 360)

            planet_diff.jupiter_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[6]))
            if planet_diff.jupiter_diff > 180:
                planet_diff.jupiter_diff = abs(abs(planet_diff.jupiter_diff) - 360)

            planet_diff.saturn_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[7]))
            if planet_diff.saturn_diff > 180:
                planet_diff.saturn_diff = abs(abs(planet_diff.saturn_diff) - 360)

            planet_diff.uranus_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[8]))
            if planet_diff.uranus_diff > 180:
                planet_diff.uranus_diff = abs(abs(planet_diff.uranus_diff) - 360)

            planet_diff.neptune_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[9]))
            if planet_diff.neptune_diff > 180:
                planet_diff.neptune_diff = abs(abs(planet_diff.neptune_diff) - 360)

            planet_diff.pluto_diff = abs(float(self.terry_planets[j]) - float(self.current_planets[10]))
            print("Pluto Diff with index = ", j, " Diff = ", planet_diff.pluto_diff)
            if planet_diff.pluto_diff > 180:
                planet_diff.pluto_diff = abs(abs(planet_diff.pluto_diff) - 360)

            planet_diff.marker_diff = abs(float(self.terry_planets[j]) - marker_right)
            print("Marker Planet with index = ", j, " Planet = ", float(self.terry_planets[j]))
            print("Marker with index = ", j, " marker_right = ", marker_right)
            print("Marker Diff with index = ", j, " Diff = ", planet_diff.marker_diff)
            if planet_diff.marker_diff > 180:
                planet_diff.marker_diff = abs(abs(planet_diff.marker_diff) - 360)

            planet_diff.sun_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[1]))
            if planet_diff.sun_diff_cur > 180:
                planet_diff.sun_diff_cur = abs(abs(planet_diff.sun_diff_cur) - 360)

            planet_diff.moon_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[2]))
            if planet_diff.moon_diff_cur > 180:
                planet_diff.moon_diff_cur = abs(abs(planet_diff.moon_diff_cur) - 360)

            planet_diff.mercury_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[3]))
            if planet_diff.mercury_diff_cur > 180:
                planet_diff.mercury_diff_cur = abs(abs(planet_diff.mercury_diff_cur) - 360)

            planet_diff.venus_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[4]))
            if planet_diff.venus_diff_cur > 180:
                planet_diff.venus_diff_cur = abs(abs(planet_diff.venus_diff_cur) - 360)

            planet_diff.mars_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[5]))
            if planet_diff.mars_diff_cur > 180:
                planet_diff.mars_diff_cur = abs(abs(planet_diff.mars_diff_cur) - 360)

            planet_diff.jupiter_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[6]))
            if planet_diff.jupiter_diff_cur > 180:
                planet_diff.jupiter_diff_cur = abs(abs(planet_diff.jupiter_diff_cur) - 360)

            planet_diff.saturn_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[7]))
            if planet_diff.saturn_diff_cur > 180:
                planet_diff.saturn_diff_cur = abs(abs(planet_diff.saturn_diff_cur) - 360)

            planet_diff.uranus_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[8]))
            if planet_diff.uranus_diff_cur > 180:
                planet_diff.uranus_diff_cur = abs(abs(planet_diff.uranus_diff_cur) - 360)

            planet_diff.neptune_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[9]))
            if planet_diff.neptune_diff_cur > 180:
                planet_diff.neptune_diff_cur = abs(abs(planet_diff.neptune_diff_cur) - 360)

            planet_diff.pluto_diff_cur = abs(float(self.current_planets[j]) - float(self.terry_planets[10]))
            print("Pluto Diff Cur with index = ", j, " Diff = ", planet_diff.pluto_diff_cur)
            if planet_diff.pluto_diff_cur > 180:
                planet_diff.pluto_diff_cur = abs(abs(planet_diff.pluto_diff_cur) - 360)

            planet_diff.marker_diff_cur = abs(float(self.current_planets[j]) - marker_left)
            print("Marker Planet Cur with index = ", j, " Planet = ", float(self.current_planets[j]))
            print("Marker Left Cur with index = ", j, " marker_left = ", marker_left)
            print("Marker Diff Cur with index = ", j, " Diff = ", planet_diff.marker_diff_cur)
            if planet_diff.marker_diff_cur > 180:
                planet_diff.marker_diff_cur = abs(abs(planet_diff.marker_diff_cur) - 360)

            self.planet_aspects.append(planet_diff)

    def _calculate_weights(self):
        """Calculate aspect weights"""
        for j in range(11):
            weights = PlanetWeightsStruct()

            # Aspect to Natal Sun
            # Calculate conjunct, sextile, square, trine, opposite aspects
            if abs(self.planet_aspects[j].sun_diff - 0) < 10:
                weights.sun_weight = 10 - abs(self.planet_aspects[j].sun_diff - 0)
                weights.sun_aspect_type = 0
                weights.total_aspect += weights.sun_weight
                weights.total_conjunct += weights.sun_weight
                weights.total_good += weights.sun_weight
                self.sun.weight = 10 - abs(self.planet_aspects[j].sun_diff - 0)
                self.sun.aspect_type = 0
                self.sun.total_aspect += weights.sun_weight
                self.sun.total_conjunct += weights.sun_weight
                self.sun.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 60) < 5:
                weights.sun_weight = 5 - abs(self.planet_aspects[j].sun_diff - 60)
                weights.sun_aspect_type = 1
                weights.total_aspect += weights.sun_weight
                weights.total_sextile += weights.sun_weight
                weights.total_good += weights.sun_weight
                self.sun.weight = 10 - abs(self.planet_aspects[j].sun_diff - 60)
                self.sun.aspect_type = 1
                self.sun.total_aspect += weights.sun_weight
                self.sun.total_sextile += weights.sun_weight
                self.sun.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 90) < 10:
                weights.sun_weight = (10 - abs(self.planet_aspects[j].sun_diff - 90)) * -1
                weights.sun_aspect_type = 2
                weights.total_aspect += weights.sun_weight
                weights.total_square += weights.sun_weight
                weights.total_bad += weights.sun_weight
                weights.total_bad += weights.sun_weight
                self.sun.weight = 10 - abs(self.planet_aspects[j].sun_diff - 90) * -1
                self.sun.aspect_type = 2
                self.sun.total_aspect += weights.sun_weight
                self.sun.total_square += weights.sun_weight
                self.sun.total_bad += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 120) < 10:
                weights.sun_weight = 10 - abs(self.planet_aspects[j].sun_diff - 120)
                weights.sun_aspect_type = 3
                weights.total_aspect += weights.sun_weight
                weights.total_trine += weights.sun_weight
                weights.total_good += weights.sun_weight
                self.sun.weight = 10 - abs(self.planet_aspects[j].sun_diff - 120)
                self.sun.aspect_type = 3
                self.sun.total_aspect += weights.sun_weight
                self.sun.total_trine += weights.sun_weight
                self.sun.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 180) < 10:
                weights.sun_weight = (10 - abs(self.planet_aspects[j].sun_diff - 180)) * -1
                weights.sun_aspect_type = 4
                weights.total_aspect += weights.sun_weight
                weights.total_opposite += weights.sun_weight
                weights.total_bad += weights.sun_weight
                self.sun.weight = 10 - abs(self.planet_aspects[j].sun_diff - 180) * -1
                self.sun.aspect_type = 4
                self.sun.total_aspect += weights.sun_weight
                self.sun.total_opposite += weights.sun_weight
                self.sun.total_bad += weights.sun_weight
            else:
                weights.sun_weight = 0
                weights.SunAspectType = 5

            # Aspect to Current Moon
            if abs(self.planet_aspects[j].moon_diff - 0) < 10:
                weights.moon_weight = 10 - abs(self.planet_aspects[j].moon_diff - 0)
                weights.moon_aspect_type = 0
                weights.total_aspect += weights.moon_weight
                weights.total_conjunct += weights.moon_weight
                weights.total_good += weights.moon_weight
                self.moon.weight = 10 - abs(self.planet_aspects[j].moon_diff - 0)
                self.moon.aspect_type = 0
                self.moon.total_aspect += weights.moon_weight
                self.moon.total_conjunct += weights.moon_weight
                self.moon.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 60) < 5:
                weights.moon_weight = 5 - abs(self.planet_aspects[j].moon_diff - 60)
                weights.moon_aspect_type = 1
                weights.total_aspect += weights.moon_weight
                weights.total_sextile += weights.moon_weight
                weights.total_good += weights.moon_weight
                self.moon.weight = 10 - abs(self.planet_aspects[j].moon_diff - 60)
                self.moon.aspect_type = 1
                self.moon.total_aspect += weights.moon_weight
                self.moon.total_sextile += weights.moon_weight
                self.moon.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 90) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff - 90)) * -1
                weights.moon_aspect_type = 2
                weights.total_aspect += weights.moon_weight
                weights.total_square += weights.moon_weight
                weights.total_bad += weights.moon_weight
                weights.total_bad += weights.moon_weight
                self.moon.weight = 10 - abs(self.planet_aspects[j].moon_diff - 90) * -1
                self.moon.aspect_type = 2
                self.moon.total_aspect += weights.moon_weight
                self.moon.total_square += weights.moon_weight
                self.moon.total_bad += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 120) < 10:
                weights.moon_weight = 10 - abs(self.planet_aspects[j].moon_diff - 120)
                weights.moon_aspect_type = 3
                weights.total_aspect += weights.moon_weight
                weights.total_trine += weights.moon_weight
                weights.total_good += weights.moon_weight
                self.moon.weight = 10 - abs(self.planet_aspects[j].moon_diff - 120)
                self.moon.aspect_type = 3
                self.moon.total_aspect += weights.moon_weight
                self.moon.total_trine += weights.moon_weight
                self.moon.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 180) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff - 180)) * -1
                weights.moon_aspect_type = 4
                weights.total_aspect += weights.moon_weight
                weights.total_opposite += weights.moon_weight
                weights.total_bad += weights.moon_weight
                self.moon.weight = 10 - abs(self.planet_aspects[j].moon_diff - 180) * -1
                self.moon.aspect_type = 4
                self.moon.total_aspect += weights.moon_weight
                self.moon.total_opposite += weights.moon_weight
                self.moon.total_bad += weights.moon_weight
            else:
                weights.moon_weight = 0
                weights.moon_aspect_type = 5

            # Aspect to Current Venus
            if abs(self.planet_aspects[j].venus_diff - 0) < 10:
                weights.venus_weight = 10 - (abs(self.planet_aspects[j].venus_diff - 0))
                weights.venus_aspect_type = 0
                weights.total_aspect += weights.venus_weight
                weights.total_conjunct += weights.venus_weight
                weights.total_good += weights.venus_weight
                self.venus.weight = 10 - abs(self.planet_aspects[j].venus_diff - 0)
                self.venus.aspect_type = 0
                self.venus.total_aspect += weights.venus_weight
                self.venus.total_conjunct += weights.venus_weight
                self.venus.total_good += weights.venus_weight
            elif abs(self.planet_aspects[j].venus_diff - 60) < 5:
                weights.venus_weight = 5 - (abs(self.planet_aspects[j].venus_diff - 60))
                weights.venus_aspect_type = 1
                weights.total_aspect += weights.venus_weight
                weights.total_sextile += weights.venus_weight
                weights.total_good += weights.venus_weight
                self.venus.weight = 10 - abs(self.planet_aspects[j].venus_diff - 60)
                self.venus.aspect_type = 1
                self.venus.total_aspect += weights.venus_weight
                self.venus.total_conjunct += weights.venus_weight
                self.venus.total_good += weights.venus_weight

            elif abs(self.planet_aspects[j].venus_diff - 90) < 10:
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff - 90))) * -1
                weights.venus_aspect_type = 2
                weights.total_aspect += weights.venus_weight
                weights.total_square += weights.venus_weight
                weights.total_bad += weights.venus_weight
                self.venus.weight = 10 - abs(self.planet_aspects[j].venus_diff - 90) * -1
                self.venus.aspect_type = 2
                self.venus.total_aspect += weights.venus_weight
                self.venus.total_conjunct += weights.venus_weight
                self.venus.total_bad += weights.venus_weight

            elif abs(self.planet_aspects[j].venus_diff - 120) < 10:
                weights.venus_weight = 10 - (abs(self.planet_aspects[j].venus_diff - 120))
                weights.venus_aspect_type = 3
                weights.total_aspect += weights.venus_weight
                weights.total_trine += weights.venus_weight
                weights.total_good += weights.venus_weight
                self.venus.weight = 10 - abs(self.planet_aspects[j].venus_diff - 120)
                self.venus.aspect_type = 3
                self.venus.total_aspect += weights.venus_weight
                self.venus.total_conjunct += weights.venus_weight
                self.venus.total_good += weights.venus_weight

            elif abs(self.planet_aspects[j].venus_diff - 180) < 10:
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff - 180))) * -1
                weights.venus_aspect_type = 4
                weights.total_aspect += weights.venus_weight
                weights.total_opposite += weights.venus_weight
                weights.total_bad += weights.venus_weight
                self.venus.weight = 10 - abs(self.planet_aspects[j].venus_diff - 180) * -1
                self.venus.aspect_type = 4
                self.venus.total_aspect += weights.venus_weight
                self.venus.total_conjunct += weights.venus_weight
                self.venus.total_bad += weights.venus_weight
            else:
                weights.venus_weight = 0
                weights.venus_aspect_type = 5

            # Aspect to Current Mercury
            if abs(self.planet_aspects[j].mercury_diff - 0) < 10:
                weights.mercury_weight = 10 - (abs(self.planet_aspects[j].mercury_diff - 0))
                weights.mercury_aspect_type = 0
                weights.total_aspect += weights.mercury_weight
                weights.total_conjunct += weights.mercury_weight
                weights.total_good += weights.mercury_weight
                self.mercury.weight = 10 - abs(self.planet_aspects[j].mercury_diff - 0)
                self.mercury.aspect_type = 0
                self.mercury.total_aspect += weights.mercury_weight
                self.mercury.total_conjunct += weights.mercury_weight
                self.mercury.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff - 60) < 5:
                weights.mercury_weight = 5 - (abs(self.planet_aspects[j].mercury_diff - 60))
                weights.mercury_aspect_type = 1
                weights.total_aspect += weights.mercury_weight
                weights.total_sextile += weights.mercury_weight
                weights.total_good += weights.mercury_weight
                self.mercury.weight = 10 - abs(self.planet_aspects[j].mercury_diff - 60)
                self.mercury.aspect_type = 1
                self.mercury.total_aspect += weights.mercury_weight
                self.mercury.total_sextile += weights.mercury_weight
                self.mercury.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff - 90) < 10:
                weights.mercury_weight = (10 - (abs(self.planet_aspects[j].mercury_diff - 90))) * -1
                weights.mercury_aspect_type = 2
                weights.total_aspect += weights.mercury_weight
                weights.total_square += weights.mercury_weight
                weights.total_bad += weights.mercury_weight
                self.mercury.weight = 10 - abs(self.planet_aspects[j].mercury_diff - 90) * -1
                self.mercury.aspect_type = 2
                self.mercury.total_aspect += weights.mercury_weight
                self.mercury.total_square += weights.mercury_weight
                self.mercury.total_bad += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff - 120) < 10:
                weights.mercury_weight = 10 - (abs(self.planet_aspects[j].mercury_diff - 120))
                weights.mercury_aspect_type = 3
                weights.total_aspect += weights.mercury_weight
                weights.total_trine += weights.mercury_weight
                weights.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff - 180) < 10:
                weights.mercury_weight = (10 - (abs(self.planet_aspects[j].mercury_diff - 180))) * -1
                weights.mercury_aspect_type = 4
                weights.total_aspect += weights.mercury_weight
                weights.total_opposite += weights.mercury_weight
                weights.total_bad += weights.mercury_weight
                self.mercury.weight = 10 - abs(self.planet_aspects[j].mercury_diff - 180) * -1
                self.mercury.aspect_type = 4
                self.mercury.total_aspect += weights.mercury_weight
                self.mercury.total_opposite += weights.mercury_weight
                self.mercury.total_bad += weights.mercury_weight
            else:
                weights.mercury_weight = 0
                weights.mercury_aspect_type = 5


            # Aspect to Current Mars
            if abs(self.planet_aspects[j].mars_diff - 0) < 10:
                weights.mars_weight = 10 - (abs(self.planet_aspects[j].mars_diff - 0))
                weights.mars_aspect_type = 0
                weights.total_aspect += weights.mars_weight
                weights.total_conjunct += weights.mars_weight
                weights.total_good += weights.mars_weight
                self.mars.weight = 10 - abs(self.planet_aspects[j].mars_diff - 0)
                self.mars.aspect_type = 0
                self.mars.total_aspect += weights.mars_weight
                self.mars.total_conjunct += weights.mars_weight
                self.mars.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff - 60) < 5:
                weights.mars_weight = 5 - (abs(self.planet_aspects[j].mars_diff - 60))
                weights.mars_aspect_type = 1
                weights.total_aspect += weights.mars_weight
                weights.total_sextile += weights.mars_weight
                weights.total_good += weights.mars_weight
                self.mars.weight = 10 - abs(self.planet_aspects[j].mars_diff - 60)
                self.mars.aspect_type = 1
                self.mars.total_aspect += weights.mars_weight
                self.mars.total_sextile += weights.mars_weight
                self.mars.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff - 90) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff - 90))) * -1
                weights.mars_aspect_type = 2
                weights.total_aspect += weights.mars_weight
                weights.total_square += weights.mars_weight
                weights.total_bad += weights.mars_weight
                self.mars.weight = 10 - abs(self.planet_aspects[j].mars_diff - 90) * -1
                self.mars.aspect_type = 2
                self.mars.total_aspect += weights.mars_weight
                self.mars.total_square += weights.mars_weight
                self.mars.total_bad += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff - 120) < 10:
                weights.mars_weight = 10 - (abs(self.planet_aspects[j].mars_diff - 120))
                weights.mars_aspect_type = 3
                weights.total_aspect += weights.mars_weight
                weights.total_trine += weights.mars_weight
                weights.total_good += weights.mars_weight
                self.mars.weight = 10 - abs(self.planet_aspects[j].mars_diff - 120)
                self.mars.aspect_type = 3
                self.mars.total_aspect += weights.mars_weight
                self.mars.total_trine += weights.mars_weight
                self.mars.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff - 180) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff - 180))) * -1
                weights.mars_aspect_type = 4
                weights.total_aspect += weights.mars_weight
                weights.total_opposite += weights.mars_weight
                weights.total_bad += weights.mars_weight
                self.mars.weight = 10 - abs(self.planet_aspects[j].mars_diff - 180) * -1
                self.mars.aspect_type = 4
                self.mars.total_aspect += weights.mars_weight
                self.mars.total_opposite += weights.mars_weight
                self.mars.total_bad += weights.mars_weight
            else:
                weights.mars_weight = 0
                weights.mars_aspect_type = 5

            # Aspect to Current Jupiter
            if abs(self.planet_aspects[j].jupiter_diff - 0) < 10:
                weights.jupiter_weight = 10 - (abs(self.planet_aspects[j].jupiter_diff - 0))
                weights.jupiter_aspect_type = 0
                weights.total_aspect += weights.jupiter_weight
                weights.total_conjunct += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
                self.jupiter.weight = 10 - abs(self.planet_aspects[j].jupiter_diff - 0)
                self.jupiter.aspect_type = 0
                self.jupiter.total_aspect += weights.jupiter_weight
                self.jupiter.total_conjunct += weights.jupiter_weight
                self.jupiter.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff - 60) < 5:
                weights.jupiter_weight = 5 - (abs(self.planet_aspects[j].jupiter_diff - 60))
                weights.jupiter_aspect_type = 1
                weights.total_aspect += weights.jupiter_weight
                weights.total_sextile += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
                self.jupiter.weight = 10 - abs(self.planet_aspects[j].jupiter_diff - 60)
                self.jupiter.aspect_type = 1
                self.jupiter.total_aspect += weights.jupiter_weight
                self.jupiter.total_sextile += weights.jupiter_weight
                self.jupiter.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff - 90) < 10:
                weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff - 90))) * -1
                weights.jupiter_aspect_type = 2
                weights.total_aspect += weights.jupiter_weight
                weights.total_square += weights.jupiter_weight
                weights.total_bad += weights.jupiter_weight
                self.jupiter.weight = 10 - abs(self.planet_aspects[j].jupiter_diff - 90) * -1
                self.jupiter.aspect_type = 2
                self.jupiter.total_aspect += weights.jupiter_weight
                self.jupiter.total_square += weights.jupiter_weight
                self.jupiter.total_bad += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff - 120) < 10:
                weights.jupiter_weight = 10 - (abs(self.planet_aspects[j].jupiter_diff - 120))
                weights.jupiter_aspect_type = 3
                weights.total_aspect += weights.jupiter_weight
                weights.total_trine += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
                self.jupiter.weight = 10 - abs(self.planet_aspects[j].jupiter_diff - 120)
                self.jupiter.aspect_type = 3
                self.jupiter.total_aspect += weights.jupiter_weight
                self.jupiter.total_trine += weights.jupiter_weight
                self.jupiter.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff - 180) < 10:
                weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff - 180))) * -1
                weights.jupiter_aspect_type = 4
                weights.total_aspect += weights.jupiter_weight
                weights.total_opposite += weights.jupiter_weight
                weights.total_bad += weights.jupiter_weight
                self.jupiter.weight = 10 - abs(self.planet_aspects[j].jupiter_diff - 180) * -1
                self.jupiter.aspect_type = 4
                self.jupiter.total_aspect += weights.jupiter_weight
                self.jupiter.total_opposite += weights.jupiter_weight
                self.jupiter.total_bad += weights.jupiter_weight
            else:
               weights.jupiter_weight = 0
               weights.jupiter_aspect_type = 5

           # Aspect to Current Saturn
            if abs(self.planet_aspects[j].saturn_diff - 0) < 10:
                weights.saturn_weight = 10 - (abs(self.planet_aspects[j].saturn_diff - 0))
                weights.saturn_aspect_type = 0
                weights.total_aspect += weights.saturn_weight
                weights.total_conjunct += weights.saturn_weight
                weights.total_good += weights.saturn_weight
                self.saturn.weight = 10 - abs(self.planet_aspects[j].saturn_diff - 0)
                self.saturn.aspect_type = 0
                self.saturn.total_aspect += weights.saturn_weight
                self.saturn.total_conjunct += weights.saturn_weight
                self.saturn.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff - 60) < 5:
                weights.saturn_weight = 5 - (abs(self.planet_aspects[j].saturn_diff - 60))
                weights.saturn_aspect_type = 1
                weights.total_aspect += weights.saturn_weight
                weights.total_sextile += weights.saturn_weight
                weights.total_good += weights.saturn_weight
                self.saturn.weight = 10 - abs(self.planet_aspects[j].saturn_diff - 60)
                self.saturn.aspect_type = 1
                self.saturn.total_aspect += weights.saturn_weight
                self.saturn.total_sextile += weights.saturn_weight
                self.saturn.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff - 90) < 10:
                weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff - 90))) * -1
                weights.saturn_aspect_type = 2
                weights.total_aspect += weights.saturn_weight
                weights.total_square += weights.saturn_weight
                weights.total_bad += weights.saturn_weight
                self.saturn.weight = 10 - abs(self.planet_aspects[j].saturn_diff - 90) * -1
                self.saturn.aspect_type = 2
                self.saturn.total_aspect += weights.saturn_weight
                self.saturn.total_square += weights.saturn_weight
                self.saturn.total_bad += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff - 120) < 10:
                weights.saturn_weight = 10 - (abs(self.planet_aspects[j].saturn_diff - 120))
                weights.saturn_aspect_type = 3
                weights.total_aspect += weights.saturn_weight
                weights.total_trine += weights.saturn_weight
                weights.total_good += weights.saturn_weight
                self.saturn.weight = 10 - abs(self.planet_aspects[j].saturn_diff - 120)
                self.saturn.aspect_type = 3
                self.saturn.total_aspect += weights.saturn_weight
                self.saturn.total_trine += weights.saturn_weight
                self.saturn.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff - 180) < 10:
                weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff - 180))) * -1
                weights.saturn_aspect_type = 4
                weights.total_aspect += weights.saturn_weight
                weights.total_opposite += weights.saturn_weight
                weights.total_bad += weights.saturn_weight
                self.saturn.weight = 10 - abs(self.planet_aspects[j].saturn_diff - 180) * -1
                self.saturn.aspect_type = 4
                self.saturn.total_aspect += weights.saturn_weight
                self.saturn.total_opposite += weights.saturn_weight
                self.saturn.total_bad += weights.saturn_weight
            else:
               weights.saturn_weight = 0
               weights.saturn_aspect_type = 5

            # Aspect to Current Uranus
            if abs(self.planet_aspects[j].uranus_diff - 0) < 10:
                weights.uranus_weight = 10 - (abs(self.planet_aspects[j].uranus_diff - 0))
                weights.uranus_aspect_type = 0
                weights.total_aspect += weights.uranus_weight
                weights.total_conjunct += weights.uranus_weight
                weights.total_good += weights.uranus_weight
                self.uranus.weight = 10 - abs(self.planet_aspects[j].uranus_diff - 0)
                self.uranus.aspect_type = 0
                self.uranus.total_aspect += weights.uranus_weight
                self.uranus.total_conjunct += weights.uranus_weight
                self.uranus.total_good += weights.uranus_weight
            elif abs(self.planet_aspects[j].uranus_diff - 60) < 5:
                weights.uranus_weight = 5 - (abs(self.planet_aspects[j].uranus_diff - 60))
                weights.uranus_aspect_type = 1
                weights.total_aspect += weights.uranus_weight
                weights.total_sextile += weights.uranus_weight
                weights.total_good += weights.uranus_weight
                self.uranus.weight = 10 - abs(self.planet_aspects[j].uranus_diff - 60)
                self.uranus.aspect_type = 1
                self.uranus.total_aspect += weights.uranus_weight
                self.uranus.total_sextile += weights.uranus_weight
                self.uranus.total_good += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff - 90) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff - 90))) * -1
                weights.uranus_aspect_type = 2
                weights.total_aspect += weights.uranus_weight
                weights.total_square += weights.uranus_weight
                weights.total_bad += weights.uranus_weight
                self.uranus.weight = 10 - abs(self.planet_aspects[j].uranus_diff - 90) * -1
                self.uranus.aspect_type = 2
                self.uranus.total_aspect += weights.uranus_weight
                self.uranus.total_square += weights.uranus_weight
                self.uranus.total_bad += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff - 120) < 10:
                weights.uranus_weight = 10 - (abs(self.planet_aspects[j].uranus_diff - 120))
                weights.uranus_aspect_type = 3
                weights.total_aspect += weights.uranus_weight
                weights.total_trine += weights.uranus_weight
                weights.total_good += weights.uranus_weight
                self.uranus.weight = 10 - abs(self.planet_aspects[j].uranus_diff - 120)
                self.uranus.aspect_type = 3
                self.uranus.total_aspect += weights.uranus_weight
                self.uranus.total_trine += weights.uranus_weight
                self.uranus.total_good += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff - 180) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff - 180))) * -1
                weights.uranus_aspect_type = 4
                weights.total_aspect += weights.uranus_weight
                weights.total_opposite += weights.uranus_weight
                weights.total_bad += weights.uranus_weight
                self.uranus.weight = 10 - abs(self.planet_aspects[j].uranus_diff - 180) * -1
                self.uranus.aspect_type = 4
                self.uranus.total_aspect += weights.uranus_weight
                self.uranus.total_opposite += weights.uranus_weight
                self.uranus.total_bad += weights.uranus_weight
            else:
                weights.uranus_weight = 0
                weights.uranus_aspect_type = 5

            # Aspect to Current Neptune
            if abs(self.planet_aspects[j].neptune_diff - 0) < 10:
                weights.neptune_weight = 10 - (abs(self.planet_aspects[j].neptune_diff - 0))
                weights.neptune_aspect_type = 0
                weights.total_aspect += weights.neptune_weight
                weights.total_conjunct += weights.neptune_weight
                weights.total_good += weights.neptune_weight
                self.neptune.weight = 10 - abs(self.planet_aspects[j].neptune_diff - 0)
                self.neptune.aspect_type = 0
                self.neptune.total_aspect += weights.neptune_weight
                self.neptune.total_conjunct += weights.neptune_weight
                self.neptune.total_good += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff - 60) < 5:
                weights.neptune_weight = 5 - (abs(self.planet_aspects[j].neptune_diff - 60))
                weights.neptune_aspect_type = 1
                weights.total_aspect += weights.neptune_weight
                weights.total_sextile += weights.neptune_weight
                weights.total_good += weights.neptune_weight
                self.neptune.weight = 10 - abs(self.planet_aspects[j].neptune_diff - 60)
                self.neptune.aspect_type = 1
                self.neptune.total_aspect += weights.neptune_weight
                self.neptune.total_sextile += weights.neptune_weight
                self.neptune.total_good += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff - 90) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff - 90))) * -1
                weights.neptune_aspect_type = 2
                weights.total_aspect += weights.neptune_weight
                weights.total_square += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
                self.neptune.weight = 10 - abs(self.planet_aspects[j].neptune_diff - 90) * -1
                self.neptune.aspect_type = 2
                self.neptune.total_aspect += weights.neptune_weight
                self.neptune.total_square += weights.neptune_weight
                self.neptune.total_bad += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff - 120) < 10:
                weights.neptune_weight = 10 - (abs(self.planet_aspects[j].neptune_diff - 120))
                weights.neptune_aspect_type = 3
                weights.total_aspect += weights.neptune_weight
                weights.total_trine += weights.neptune_weight
                weights.total_good += weights.neptune_weight
                self.neptune.weight = 10 - abs(self.planet_aspects[j].neptune_diff - 120)
                self.neptune.aspect_type = 3
                self.neptune.total_aspect += weights.neptune_weight
                self.neptune.total_trine += weights.neptune_weight
                self.neptune.total_good += weights.neptune_weight

            elif abs(self.planet_aspects[j].neptune_diff - 180) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff - 180))) * -1
                weights.neptune_aspect_type = 4
                weights.total_aspect += weights.neptune_weight
                weights.total_opposite += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
                self.neptune.weight = 10 - abs(self.planet_aspects[j].neptune_diff - 180) * -1
                self.neptune.aspect_type = 4
                self.neptune.total_aspect += weights.neptune_weight
                self.neptune.total_opposite += weights.neptune_weight
                self.neptune.total_bad += weights.neptune_weight
            else:
                weights.neptune_weight = 0
                weights.neptune_aspect_type = 5

            # Aspect to Current Pluto
            if abs(self.planet_aspects[j].pluto_diff - 0) < 10:
                weights.pluto_weight = 10 - (abs(self.planet_aspects[j].pluto_diff - 0))
                weights.pluto_aspect_type = 0
                weights.total_aspect += weights.pluto_weight
                weights.total_conjunct += weights.pluto_weight
                weights.total_good += weights.pluto_weight
                self.pluto.weight = 10 - abs(self.planet_aspects[j].pluto_diff - 0)
                self.pluto.aspect_type = 0
                self.pluto.total_aspect += weights.pluto_weight
                self.pluto.total_conjunct += weights.pluto_weight
                self.pluto.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff - 60) < 5:
                weights.pluto_weight = 5 - (abs(self.planet_aspects[j].pluto_diff - 60))
                weights.pluto_aspect_type = 1
                weights.total_aspect += weights.pluto_weight
                weights.total_sextile += weights.pluto_weight
                weights.total_good += weights.pluto_weight
                self.pluto.weight = 10 - abs(self.planet_aspects[j].pluto_diff - 60)
                self.pluto.aspect_type = 1
                self.pluto.total_aspect += weights.pluto_weight
                self.pluto.total_sextile += weights.pluto_weight
                self.pluto.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff - 90) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff - 90))) * -1
                weights.pluto_aspect_type = 2
                weights.total_aspect += weights.pluto_weight
                weights.total_square += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
                self.pluto.weight = 10 - abs(self.planet_aspects[j].pluto_diff - 90) * -1
                self.pluto.aspect_type = 2
                self.pluto.total_aspect += weights.pluto_weight
                self.pluto.total_square += weights.pluto_weight
                self.pluto.total_bad += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff - 120) < 10:
                weights.pluto_weight = 10 - (abs(self.planet_aspects[j].pluto_diff - 120))
                weights.pluto_aspect_type = 3
                weights.total_aspect += weights.pluto_weight
                weights.total_trine += weights.pluto_weight
                weights.total_good += weights.pluto_weight
                self.pluto.weight = 10 - abs(self.planet_aspects[j].pluto_diff - 120)
                self.pluto.aspect_type = 3
                self.pluto.total_aspect += weights.pluto_weight
                self.pluto.total_trine += weights.pluto_weight
                self.pluto.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff - 180) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff - 180))) * -1
                weights.pluto_aspect_type = 4
                weights.total_aspect += weights.pluto_weight
                weights.total_opposite += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
                self.pluto.weight = 10 - abs(self.planet_aspects[j].pluto_diff - 180) * -1
                self.pluto.aspect_type = 4
                self.pluto.total_aspect += weights.pluto_weight
                self.pluto.total_opposite += weights.pluto_weight
                self.pluto.total_bad += weights.pluto_weight
            else:
                weights.pluto_weight = 0
                weights.pluto_aspect_type = 5

            # Aspect to Marker Right
            if abs(self.planet_aspects[j].marker_diff - 0) < 10:
                weights.marker_weight = 10 - (abs(self.planet_aspects[j].marker_diff - 0))
                weights.marker_aspect_type = 0
                weights.marker_aspect += weights.marker_weight
                weights.marker_conjunct += weights.marker_weight
                weights.marker_good += weights.marker_weight
                self.marker.weight = 10 - abs(self.planet_aspects[j].marker_diff - 0)
                self.marker.aspect_type = 0
                self.marker.total_aspect += weights.marker_weight
                self.marker.total_conjunct += weights.marker_weight
                self.marker.total_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff - 60) < 5:
                weights.marker_weight = 5 - (abs(self.planet_aspects[j].marker_diff - 60))
                weights.marker_aspect_type = 1
                weights.marker_aspect += weights.marker_weight
                weights.marker_sextile += weights.marker_weight
                weights.marker_good += weights.marker_weight
                self.marker.weight = 10 - abs(self.planet_aspects[j].marker_diff - 60)
                self.marker.aspect_type = 1
                self.marker.total_aspect += weights.marker_weight
                self.marker.total_sextile += weights.marker_weight
                self.marker.total_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff - 90) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff - 90))) * -1
                weights.marker_aspect_type = 2
                weights.marker_aspect += weights.marker_weight
                weights.marker_square += weights.marker_weight
                weights.marker_bad += weights.marker_weight
                self.marker.weight = 10 - abs(self.planet_aspects[j].marker_diff - 90) * -1
                self.marker.aspect_type = 2
                self.marker.total_aspect += weights.marker_weight
                self.marker.total_square += weights.marker_weight
                self.marker.total_bad += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff - 120) < 10:
                weights.marker_weight = 10 - (abs(self.planet_aspects[j].marker_diff - 120))
                weights.marker_aspect_type = 3
                weights.marker_aspect += weights.marker_weight
                weights.marker_trine += weights.marker_weight
                weights.marker_good += weights.marker_weight
                self.marker.weight = 10 - abs(self.planet_aspects[j].marker_diff - 120)
                self.marker.aspect_type = 3
                self.marker.total_aspect += weights.marker_weight
                self.marker.total_trine += weights.marker_weight
                self.marker.total_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff - 180) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff - 180))) * -1
                weights.marker_aspect_type = 4
                weights.marker_aspect += weights.marker_weight
                weights.marker_opposite += weights.marker_weight
                weights.marker_bad += weights.marker_weight
                self.marker.weight = 10 - abs(self.planet_aspects[j].marker_diff - 180) * -1
                self.marker.aspect_type = 4
                self.marker.total_aspect += weights.marker_weight
                self.marker.total_opposite += weights.marker_weight
                self.marker.total_bad += weights.marker_weight
            else:
                weights.marker_weight = 0
                weights.marker_aspect_type = 5

            self.natal_weight_list.append(weights)


            weights = PlanetWeightsStruct()

            # Aspect to Current Sun
            # Calculate conjunct, sextile, square, trine, opposite aspects
            if abs(self.planet_aspects[j].sun_diff_cur - 0) < 10:
                weights.sun_weight = 10 - abs(self.planet_aspects[j].sun_diff_cur - 0)
                weights.sun_aspect_type = 0
                weights.total_aspect += weights.sun_weight
                weights.total_conjunct += weights.sun_weight
                weights.total_good += weights.sun_weight
                self.sun_cur.weight = 10 - abs(self.planet_aspects[j].sun_diff_cur - 0)
                self.sun_cur.aspect_type = 0
                self.sun_cur.total_aspect += weights.sun_weight
                self.sun_cur.total_conjunct += weights.sun_weight
                self.sun_cur.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 60) < 5:
                weights.sun_weight = 5 - abs(self.planet_aspects[j].sun_diff_cur - 60)
                weights.sun_aspect_type = 1
                weights.total_aspect += weights.sun_weight
                weights.total_sextile += weights.sun_weight
                weights.total_good += weights.sun_weight
                self.sun_cur.weight = 10 - abs(self.planet_aspects[j].sun_diff_cur - 60)
                self.sun_cur.aspect_type = 1
                self.sun_cur.total_aspect += weights.sun_weight
                self.sun_cur.total_sextile += weights.sun_weight
                self.sun_cur.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 90) < 10:
                weights.sun_weight = (10 - abs(self.planet_aspects[j].sun_diff_cur - 90)) * -1
                weights.sun_aspect_type = 2
                weights.total_aspect += weights.sun_weight
                weights.total_square += weights.sun_weight
                weights.total_bad += weights.sun_weight
                weights.total_bad += weights.sun_weight
                self.sun_cur.weight = 10 - abs(self.planet_aspects[j].sun_diff_cur - 90) * -1
                self.sun_cur.aspect_type = 2
                self.sun_cur.total_aspect += weights.sun_weight
                self.sun_cur.total_square += weights.sun_weight
                self.sun_cur.total_bad += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 120) < 10:
                weights.sun_weight = 10 - abs(self.planet_aspects[j].sun_diff_cur - 120)
                weights.sun_aspect_type = 3
                weights.total_aspect += weights.sun_weight
                weights.total_trine += weights.sun_weight
                weights.total_good += weights.sun_weight
                self.sun_cur.weight = 10 - abs(self.planet_aspects[j].sun_diff_cur - 120)
                self.sun_cur.aspect_type = 3
                self.sun_cur.total_aspect += weights.sun_weight
                self.sun_cur.total_trine += weights.sun_weight
                self.sun_cur.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 180) < 10:
                weights.sun_weight = (10 - abs(self.planet_aspects[j].sun_diff_cur - 180)) * -1
                weights.sun_aspect_type = 4
                weights.total_aspect += weights.sun_weight
                weights.total_opposite += weights.sun_weight
                weights.total_bad += weights.sun_weight
                self.sun_cur.weight = 10 - abs(self.planet_aspects[j].sun_diff_cur - 180) * -1
                self.sun_cur.aspect_type = 4
                self.sun_cur.total_aspect += weights.sun_weight
                self.sun_cur.total_opposite += weights.sun_weight
                self.sun_cur.total_bad += weights.sun_weight
            else:
                weights.sun_weight = 0
                weights.SunAspectType = 5

            # Aspect to Current Moon
            if abs(self.planet_aspects[j].moon_diff_cur - 0) < 10:
                weights.moon_weight = 10 - abs(self.planet_aspects[j].moon_diff_cur - 0)
                weights.moon_aspect_type = 0
                weights.total_aspect += weights.moon_weight
                weights.total_conjunct += weights.moon_weight
                weights.total_good += weights.moon_weight
                self.moon_cur.weight = 10 - abs(self.planet_aspects[j].moon_diff_cur - 0)
                self.moon_cur.aspect_type = 0
                self.moon_cur.total_aspect += weights.moon_weight
                self.moon_cur.total_conjunct += weights.moon_weight
                self.moon_cur.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff_cur - 60) < 5:
                weights.moon_weight = 5 - abs(self.planet_aspects[j].moon_diff_cur - 60)
                weights.moon_aspect_type = 1
                weights.total_aspect += weights.moon_weight
                weights.total_sextile += weights.moon_weight
                weights.total_good += weights.moon_weight
                self.moon_cur.weight = 10 - abs(self.planet_aspects[j].moon_diff_cur - 60)
                self.moon_cur.aspect_type = 1
                self.moon_cur.total_aspect += weights.moon_weight
                self.moon_cur.total_sextile += weights.moon_weight
                self.moon_cur.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff_cur - 90) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff_cur - 90)) * -1
                weights.moon_aspect_type = 2
                weights.total_aspect += weights.moon_weight
                weights.total_square += weights.moon_weight
                weights.total_bad += weights.moon_weight
                weights.total_bad += weights.moon_weight
                self.moon_cur.weight = 10 - abs(self.planet_aspects[j].moon_diff_cur - 90) * -1
                self.moon_cur.aspect_type = 2
                self.moon_cur.total_aspect += weights.moon_weight
                self.moon_cur.total_square += weights.moon_weight
                self.moon_cur.total_bad += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff_cur - 120) < 10:
                weights.moon_weight = 10 - abs(self.planet_aspects[j].moon_diff_cur - 120)
                weights.moon_aspect_type = 3
                weights.total_aspect += weights.moon_weight
                weights.total_trine += weights.moon_weight
                weights.total_good += weights.moon_weight
                self.moon_cur.weight = 10 - abs(self.planet_aspects[j].moon_diff_cur - 120)
                self.moon_cur.aspect_type = 3
                self.moon_cur.total_aspect += weights.moon_weight
                self.moon_cur.total_trine += weights.moon_weight
                self.moon_cur.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff_cur - 180) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff_cur - 180)) * -1
                weights.moon_aspect_type = 4
                weights.total_aspect += weights.moon_weight
                weights.total_opposite += weights.moon_weight
                weights.total_bad += weights.moon_weight
                self.moon_cur.weight = 10 - abs(self.planet_aspects[j].moon_diff_cur - 180) * -1
                self.moon_cur.aspect_type = 4
                self.moon_cur.total_aspect += weights.moon_weight
                self.moon_cur.total_opposite += weights.moon_weight
                self.moon_cur.total_bad += weights.moon_weight
            else:
                weights.moon_weight = 0
                weights.moon_aspect_type = 5

            # Aspect to Current Venus
            if abs(self.planet_aspects[j].venus_diff_cur - 0) < 10:
                weights.venus_weight = 10 - (abs(self.planet_aspects[j].venus_diff_cur - 0))
                weights.venus_aspect_type = 0
                weights.total_aspect += weights.venus_weight
                weights.total_conjunct += weights.venus_weight
                weights.total_good += weights.venus_weight
                self.venus_cur.weight = 10 - abs(self.planet_aspects[j].venus_diff_cur - 0)
                self.venus_cur.aspect_type = 0
                self.venus_cur.total_aspect += weights.venus_weight
                self.venus_cur.total_conjunct += weights.venus_weight
                self.venus_cur.total_good += weights.venus_weight
            elif abs(self.planet_aspects[j].venus_diff_cur - 60) < 5:
                weights.venus_weight = 5 - (abs(self.planet_aspects[j].venus_diff_cur - 60))
                weights.venus_aspect_type = 1
                weights.total_aspect += weights.venus_weight
                weights.total_sextile += weights.venus_weight
                weights.total_good += weights.venus_weight
                self.venus_cur.weight = 10 - abs(self.planet_aspects[j].venus_diff_cur - 60)
                self.venus_cur.aspect_type = 1
                self.venus_cur.total_aspect += weights.venus_weight
                self.venus_cur.total_conjunct += weights.venus_weight
                self.venus_cur.total_good += weights.venus_weight
            elif abs(self.planet_aspects[j].venus_diff_cur - 90) < 10:
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff_cur - 90))) * -1
                weights.venus_aspect_type = 2
                weights.total_aspect += weights.venus_weight
                weights.total_square += weights.venus_weight
                weights.total_bad += weights.venus_weight
                self.venus_cur.weight = 10 - abs(self.planet_aspects[j].venus_diff_cur - 90) * -1
                self.venus_cur.aspect_type = 2
                self.venus_cur.total_aspect += weights.venus_weight
                self.venus_cur.total_conjunct += weights.venus_weight
                self.venus_cur.total_bad += weights.venus_weight
            elif abs(self.planet_aspects[j].venus_diff_cur - 120) < 10:
                weights.venus_weight = 10 - (abs(self.planet_aspects[j].venus_diff_cur - 120))
                weights.venus_aspect_type = 3
                weights.total_aspect += weights.venus_weight
                weights.total_trine += weights.venus_weight
                weights.total_good += weights.venus_weight
                self.venus_cur.weight = 10 - abs(self.planet_aspects[j].venus_diff_cur - 120)
                self.venus_cur.aspect_type = 3
                self.venus_cur.total_aspect += weights.venus_weight
                self.venus_cur.total_conjunct += weights.venus_weight
                self.venus_cur.total_good += weights.venus_weight
            elif abs(self.planet_aspects[j].venus_diff_cur - 180) < 10:
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff_cur - 180))) * -1
                weights.venus_aspect_type = 4
                weights.total_aspect += weights.venus_weight
                weights.total_opposite += weights.venus_weight
                weights.total_bad += weights.venus_weight
                self.venus_cur.weight = 10 - abs(self.planet_aspects[j].venus_diff_cur - 180) * -1
                self.venus_cur.aspect_type = 4
                self.venus_cur.total_aspect += weights.venus_weight
                self.venus_cur.total_conjunct += weights.venus_weight
                self.venus_cur.total_bad += weights.venus_weight
            else:
                weights.venus_weight = 0
                weights.venus_aspect_type = 5

            # Aspect to Current Mercury
            if abs(self.planet_aspects[j].mercury_diff_cur - 0) < 10:
                weights.mercury_weight = 10 - (abs(self.planet_aspects[j].mercury_diff_cur - 0))
                weights.mercury_aspect_type = 0
                weights.total_aspect += weights.mercury_weight
                weights.total_conjunct += weights.mercury_weight
                weights.total_good += weights.mercury_weight
                self.mercury_cur.weight = 10 - abs(self.planet_aspects[j].mercury_diff_cur - 0)
                self.mercury_cur.aspect_type = 0
                self.mercury_cur.total_aspect += weights.mercury_weight
                self.mercury_cur.total_conjunct += weights.mercury_weight
                self.mercury_cur.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 60) < 5:
                weights.mercury_weight = 5 - (abs(self.planet_aspects[j].mercury_diff_cur - 60))
                weights.mercury_aspect_type = 1
                weights.total_aspect += weights.mercury_weight
                weights.total_sextile += weights.mercury_weight
                weights.total_good += weights.mercury_weight
                self.mercury_cur.weight = 10 - abs(self.planet_aspects[j].mercury_diff_cur - 60)
                self.mercury_cur.aspect_type = 1
                self.mercury_cur.total_aspect += weights.mercury_weight
                self.mercury_cur.total_sextile += weights.mercury_weight
                self.mercury_cur.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 90) < 10:
                weights.mercury_weight = (10 - (abs(self.planet_aspects[j].mercury_diff_cur - 90))) * -1
                weights.mercury_aspect_type = 2
                weights.total_aspect += weights.mercury_weight
                weights.total_square += weights.mercury_weight
                weights.total_bad += weights.mercury_weight
                self.mercury_cur.weight = 10 - abs(self.planet_aspects[j].mercury_diff_cur - 90) * -1
                self.mercury_cur.aspect_type = 2
                self.mercury_cur.total_aspect += weights.mercury_weight
                self.mercury_cur.total_square += weights.mercury_weight
                self.mercury_cur.total_bad += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 120) < 10:
                weights.mercury_weight = 10 - (abs(self.planet_aspects[j].mercury_diff_cur - 120))
                weights.mercury_aspect_type = 3
                weights.total_aspect += weights.mercury_weight
                weights.total_trine += weights.mercury_weight
                weights.total_good += weights.mercury_weight
                self.mercury_cur.weight = 10 - abs(self.planet_aspects[j].mercury_diff_cur - 120)
                self.mercury_cur.aspect_type = 3
                self.mercury_cur.total_aspect += weights.mercury_weight
                self.mercury_cur.total_trine += weights.mercury_weight
                self.mercury_cur.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 180) < 10:
                weights.mercury_weight = (10 - (abs(self.planet_aspects[j].mercury_diff_cur - 180))) * -1
                weights.mercury_aspect_type = 4
                weights.total_aspect += weights.mercury_weight
                weights.total_opposite += weights.mercury_weight
                weights.total_bad += weights.mercury_weight
                self.mercury_cur.weight = 10 - abs(self.planet_aspects[j].mercury_diff_cur - 180) * -1
                self.mercury_cur.aspect_type = 4
                self.mercury_cur.total_aspect += weights.mercury_weight
                self.mercury_cur.total_opposite += weights.mercury_weight
                self.mercury_cur.total_bad += weights.mercury_weight
            else:
                weights.mercury_weight = 0
                weights.mercury_aspect_type = 5


            # Aspect to Current Mars
            if abs(self.planet_aspects[j].mars_diff_cur - 0) < 10:
                weights.mars_weight = 10 - (abs(self.planet_aspects[j].mars_diff_cur - 0))
                weights.mars_aspect_type = 0
                weights.total_aspect += weights.mars_weight
                weights.total_conjunct += weights.mars_weight
                weights.total_good += weights.mars_weight
                self.mars_cur.weight = 10 - abs(self.planet_aspects[j].mars_diff_cur - 0)
                self.mars_cur.aspect_type = 0
                self.mars_cur.total_aspect += weights.mars_weight
                self.mars_cur.total_conjunct += weights.mars_weight
                self.mars_cur.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff_cur - 60) < 5:
                weights.mars_weight = 5 - (abs(self.planet_aspects[j].mars_diff_cur - 60))
                weights.mars_aspect_type = 1
                weights.total_aspect += weights.mars_weight
                weights.total_sextile += weights.mars_weight
                weights.total_good += weights.mars_weight
                self.mars_cur.weight = 10 - abs(self.planet_aspects[j].mars_diff_cur - 60)
                self.mars_cur.aspect_type = 1
                self.mars_cur.total_aspect += weights.mars_weight
                self.mars_cur.total_sextile += weights.mars_weight
                self.mars_cur.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff_cur - 90) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff_cur - 90))) * -1
                weights.mars_aspect_type = 2
                weights.total_aspect += weights.mars_weight
                weights.total_square += weights.mars_weight
                weights.total_bad += weights.mars_weight
                self.mars_cur.weight = 10 - abs(self.planet_aspects[j].mars_diff_cur - 90) * -1
                self.mars_cur.aspect_type = 2
                self.mars_cur.total_aspect += weights.mars_weight
                self.mars_cur.total_square += weights.mars_weight
                self.mars_cur.total_bad += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff_cur - 120) < 10:
                weights.mars_weight = 10 - (abs(self.planet_aspects[j].mars_diff_cur - 120))
                weights.mars_aspect_type = 3
                weights.total_aspect += weights.mars_weight
                weights.total_trine += weights.mars_weight
                weights.total_good += weights.mars_weight
                self.mars_cur.weight = 10 - abs(self.planet_aspects[j].mars_diff_cur - 120)
                self.mars_cur.aspect_type = 3
                self.mars_cur.total_aspect += weights.mars_weight
                self.mars_cur.total_trine += weights.mars_weight
                self.mars_cur.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff_cur - 180) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff_cur - 180))) * -1
                weights.mars_aspect_type = 4
                weights.total_aspect += weights.mars_weight
                weights.total_opposite += weights.mars_weight
                weights.total_bad += weights.mars_weight
                self.mars_cur.weight = 10 - abs(self.planet_aspects[j].mars_diff_cur - 180) * -1
                self.mars_cur.aspect_type = 4
                self.mars_cur.total_aspect += weights.mars_weight
                self.mars_cur.total_opposite += weights.mars_weight
                self.mars_cur.total_bad += weights.mars_weight
            else:
                weights.mars_weight = 0
                weights.mars_aspect_type = 5

            # Aspect to Current Jupiter
            if abs(self.planet_aspects[j].jupiter_diff_cur - 0) < 10:
                weights.jupiter_weight = 10 - (abs(self.planet_aspects[j].jupiter_diff_cur - 0))
                weights.jupiter_aspect_type = 0
                weights.total_aspect += weights.jupiter_weight
                weights.total_conjunct += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
                self.jupiter_cur.weight = 10 - abs(self.planet_aspects[j].jupiter_diff_cur - 0)
                self.jupiter_cur.aspect_type = 0
                self.jupiter_cur.total_aspect += weights.jupiter_weight
                self.jupiter_cur.total_conjunct += weights.jupiter_weight
                self.jupiter_cur.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 60) < 5:
                weights.jupiter_weight = 5 - (abs(self.planet_aspects[j].jupiter_diff_cur - 60))
                weights.jupiter_aspect_type = 1
                weights.total_aspect += weights.jupiter_weight
                weights.total_sextile += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
                self.jupiter_cur.weight = 10 - abs(self.planet_aspects[j].jupiter_diff_cur - 60)
                self.jupiter_cur.aspect_type = 1
                self.jupiter_cur.total_aspect += weights.jupiter_weight
                self.jupiter_cur.total_sextile += weights.jupiter_weight
                self.jupiter_cur.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 90) < 10:
                weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff_cur - 90))) * -1
                weights.jupiter_aspect_type = 2
                weights.total_aspect += weights.jupiter_weight
                weights.total_square += weights.jupiter_weight
                weights.total_bad += weights.jupiter_weight
                self.jupiter_cur.weight = 10 - abs(self.planet_aspects[j].jupiter_diff_cur - 90) * -1
                self.jupiter_cur.aspect_type = 2
                self.jupiter_cur.total_aspect += weights.jupiter_weight
                self.jupiter_cur.total_square += weights.jupiter_weight
                self.jupiter_cur.total_bad += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 120) < 10:
                weights.jupiter_weight = 10 - (abs(self.planet_aspects[j].jupiter_diff_cur - 120))
                weights.jupiter_aspect_type = 3
                weights.total_aspect += weights.jupiter_weight
                weights.total_trine += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
                self.jupiter_cur.weight = 10 - abs(self.planet_aspects[j].jupiter_diff_cur - 120)
                self.jupiter_cur.aspect_type = 3
                self.jupiter_cur.total_aspect += weights.jupiter_weight
                self.jupiter_cur.total_trine += weights.jupiter_weight
                self.jupiter_cur.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 180) < 10:
                weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff_cur - 180))) * -1
                weights.jupiter_aspect_type = 4
                weights.total_aspect += weights.jupiter_weight
                weights.total_opposite += weights.jupiter_weight
                weights.total_bad += weights.jupiter_weight
                self.jupiter_cur.weight = 10 - abs(self.planet_aspects[j].jupiter_diff_cur - 180) * -1
                self.jupiter_cur.aspect_type = 4
                self.jupiter_cur.total_aspect += weights.jupiter_weight
                self.jupiter_cur.total_opposite += weights.jupiter_weight
                self.jupiter_cur.total_bad += weights.jupiter_weight
            else:
               weights.jupiter_weight = 0
               weights.jupiter_aspect_type = 5

           # Aspect to Current Saturn
            if abs(self.planet_aspects[j].saturn_diff_cur - 0) < 10:
                weights.saturn_weight = 10 - (abs(self.planet_aspects[j].saturn_diff_cur - 0))
                weights.saturn_aspect_type = 0
                weights.total_aspect += weights.saturn_weight
                weights.total_conjunct += weights.saturn_weight
                weights.total_good += weights.saturn_weight
                self.saturn_cur.weight = 10 - abs(self.planet_aspects[j].saturn_diff_cur - 0)
                self.saturn_cur.aspect_type = 0
                self.saturn_cur.total_aspect += weights.saturn_weight
                self.saturn_cur.total_conjunct += weights.saturn_weight
                self.saturn_cur.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 60) < 5:
                weights.saturn_weight = 5 - (abs(self.planet_aspects[j].saturn_diff_cur - 60))
                weights.saturn_aspect_type = 1
                weights.total_aspect += weights.saturn_weight
                weights.total_sextile += weights.saturn_weight
                weights.total_good += weights.saturn_weight
                self.saturn_cur.weight = 10 - abs(self.planet_aspects[j].saturn_diff_cur - 60)
                self.saturn_cur.aspect_type = 1
                self.saturn_cur.total_aspect += weights.saturn_weight
                self.saturn_cur.total_sextile += weights.saturn_weight
                self.saturn_cur.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 90) < 10:
                weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff_cur - 90))) * -1
                weights.saturn_aspect_type = 2
                weights.total_aspect += weights.saturn_weight
                weights.total_square += weights.saturn_weight
                weights.total_bad += weights.saturn_weight
                self.saturn_cur.weight = 10 - abs(self.planet_aspects[j].saturn_diff_cur - 90) * -1
                self.saturn_cur.aspect_type = 2
                self.saturn_cur.total_aspect += weights.saturn_weight
                self.saturn_cur.total_square += weights.saturn_weight
                self.saturn_cur.total_bad += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 120) < 10:
                weights.saturn_weight = 10 - (abs(self.planet_aspects[j].saturn_diff_cur - 120))
                weights.saturn_aspect_type = 3
                weights.total_aspect += weights.saturn_weight
                weights.total_trine += weights.saturn_weight
                weights.total_good += weights.saturn_weight
                self.saturn_cur.weight = 10 - abs(self.planet_aspects[j].saturn_diff_cur - 120)
                self.saturn_cur.aspect_type = 3
                self.saturn_cur.total_aspect += weights.saturn_weight
                self.saturn_cur.total_trine += weights.saturn_weight
                self.saturn_cur.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 180) < 10:
                weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff_cur - 180))) * -1
                weights.saturn_aspect_type = 4
                weights.total_aspect += weights.saturn_weight
                weights.total_opposite += weights.saturn_weight
                weights.total_bad += weights.saturn_weight
                self.saturn_cur.weight = 10 - abs(self.planet_aspects[j].saturn_diff_cur - 180) * -1
                self.saturn_cur.aspect_type = 4
                self.saturn_cur.total_aspect += weights.saturn_weight
                self.saturn_cur.total_opposite += weights.saturn_weight
                self.saturn_cur.total_bad += weights.saturn_weight
            else:
               weights.saturn_weight = 0
               weights.saturn_aspect_type = 5

            # Aspect to Current Uranus
            if abs(self.planet_aspects[j].uranus_diff_cur - 0) < 10:
                weights.uranus_weight = 10 - (abs(self.planet_aspects[j].uranus_diff_cur - 0))
                weights.uranus_aspect_type = 0
                weights.total_aspect += weights.uranus_weight
                weights.total_conjunct += weights.uranus_weight
                weights.total_good += weights.uranus_weight
                self.uranus_cur.weight = 10 - abs(self.planet_aspects[j].uranus_diff_cur - 0)
                self.uranus_cur.aspect_type = 0
                self.uranus_cur.total_aspect += weights.uranus_weight
                self.uranus_cur.total_conjunct += weights.uranus_weight
                self.uranus_cur.total_good += weights.uranus_weight
            elif abs(self.planet_aspects[j].uranus_diff_cur - 60) < 5:
                weights.uranus_weight = 5 - (abs(self.planet_aspects[j].uranus_diff_cur - 60))
                weights.uranus_aspect_type = 1
                weights.total_aspect += weights.uranus_weight
                weights.total_sextile += weights.uranus_weight
                weights.total_good += weights.uranus_weight
                self.uranus_cur.weight = 10 - abs(self.planet_aspects[j].uranus_diff_cur - 60)
                self.uranus_cur.aspect_type = 1
                self.uranus_cur.total_aspect += weights.uranus_weight
                self.uranus_cur.total_sextile += weights.uranus_weight
                self.uranus_cur.total_good += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff_cur - 90) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff_cur - 90))) * -1
                weights.uranus_aspect_type = 2
                weights.total_aspect += weights.uranus_weight
                weights.total_square += weights.uranus_weight
                weights.total_bad += weights.uranus_weight
                self.uranus_cur.weight = 10 - abs(self.planet_aspects[j].uranus_diff_cur - 90) * -1
                self.uranus_cur.aspect_type = 2
                self.uranus_cur.total_aspect += weights.uranus_weight
                self.uranus_cur.total_square += weights.uranus_weight
                self.uranus_cur.total_bad += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff_cur - 120) < 10:
                weights.uranus_weight = 10 - (abs(self.planet_aspects[j].uranus_diff_cur - 120))
                weights.uranus_aspect_type = 3
                weights.total_aspect += weights.uranus_weight
                weights.total_trine += weights.uranus_weight
                weights.total_good += weights.uranus_weight
                self.uranus_cur.weight = 10 - abs(self.planet_aspects[j].uranus_diff_cur - 120)
                self.uranus_cur.aspect_type = 3
                self.uranus_cur.total_aspect += weights.uranus_weight
                self.uranus_cur.total_trine += weights.uranus_weight
                self.uranus_cur.total_good += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff_cur - 180) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff_cur - 180))) * -1
                weights.uranus_aspect_type = 4
                weights.total_aspect += weights.uranus_weight
                weights.total_opposite += weights.uranus_weight
                weights.total_bad += weights.uranus_weight
                self.uranus_cur.weight = 10 - abs(self.planet_aspects[j].uranus_diff_cur - 180) * -1
                self.uranus_cur.aspect_type = 4
                self.uranus_cur.total_aspect += weights.uranus_weight
                self.uranus_cur.total_opposite += weights.uranus_weight
                self.uranus_cur.total_bad += weights.uranus_weight
            else:
                weights.uranus_weight = 0
                weights.uranus_aspect_type = 5

            # Aspect to Current Neptune
            if abs(self.planet_aspects[j].neptune_diff_cur - 0) < 10:
                weights.neptune_weight = 10 - (abs(self.planet_aspects[j].neptune_diff_cur - 0))
                weights.neptune_aspect_type = 0
                weights.total_aspect += weights.neptune_weight
                weights.total_conjunct += weights.neptune_weight
                weights.total_good += weights.neptune_weight
                self.neptune_cur.weight = 10 - abs(self.planet_aspects[j].neptune_diff_cur - 0)
                self.neptune_cur.aspect_type = 0
                self.neptune_cur.total_aspect += weights.neptune_weight
                self.neptune_cur.total_conjunct += weights.neptune_weight
                self.neptune_cur.total_good += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff_cur - 60) < 5:
                weights.neptune_weight = 5 - (abs(self.planet_aspects[j].neptune_diff_cur - 60))
                weights.neptune_aspect_type = 1
                weights.total_aspect += weights.neptune_weight
                weights.total_sextile += weights.neptune_weight
                weights.total_good += weights.neptune_weight
                self.neptune_cur.weight = 10 - abs(self.planet_aspects[j].neptune_diff_cur - 60)
                self.neptune_cur.aspect_type = 1
                self.neptune_cur.total_aspect += weights.neptune_weight
                self.neptune_cur.total_sextile += weights.neptune_weight
                self.neptune_cur.total_good += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff_cur - 90) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff_cur - 90))) * -1
                weights.neptune_aspect_type = 2
                weights.total_aspect += weights.neptune_weight
                weights.total_square += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
                self.neptune_cur.weight = 10 - abs(self.planet_aspects[j].neptune_diff_cur - 90) * -1
                self.neptune_cur.aspect_type = 2
                self.neptune_cur.total_aspect += weights.neptune_weight
                self.neptune_cur.total_square += weights.neptune_weight
                self.neptune_cur.total_bad += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff_cur - 120) < 10:
                weights.neptune_weight = 10 - (abs(self.planet_aspects[j].neptune_diff_cur - 120))
                weights.neptune_aspect_type = 3
                weights.total_aspect += weights.neptune_weight
                weights.total_trine += weights.neptune_weight
                weights.total_good += weights.neptune_weight
                self.neptune_cur.weight = 10 - abs(self.planet_aspects[j].neptune_diff_cur - 120)
                self.neptune_cur.aspect_type = 3
                self.neptune_cur.total_aspect += weights.neptune_weight
                self.neptune_cur.total_trine += weights.neptune_weight
                self.neptune_cur.total_good += weights.neptune_weight

            elif abs(self.planet_aspects[j].neptune_diff_cur - 180) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff_cur - 180))) * -1
                weights.neptune_aspect_type = 4
                weights.total_aspect += weights.neptune_weight
                weights.total_opposite += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
                self.neptune_cur.weight = 10 - abs(self.planet_aspects[j].neptune_diff_cur - 180) * -1
                self.neptune_cur.aspect_type = 4
                self.neptune_cur.total_aspect += weights.neptune_weight
                self.neptune_cur.total_opposite += weights.neptune_weight
                self.neptune_cur.total_bad += weights.neptune_weight
            else:
                weights.neptune_weight = 0
                weights.neptune_aspect_type = 5

            # Aspect to Current Pluto
            if abs(self.planet_aspects[j].pluto_diff_cur - 0) < 10:
                weights.pluto_weight = 10 - (abs(self.planet_aspects[j].pluto_diff_cur - 0))
                weights.pluto_aspect_type = 0
                weights.total_aspect += weights.pluto_weight
                weights.total_conjunct += weights.pluto_weight
                weights.total_good += weights.pluto_weight
                self.pluto_cur.weight = 10 - abs(self.planet_aspects[j].pluto_diff_cur - 0)
                self.pluto_cur.aspect_type = 0
                self.pluto_cur.total_aspect += weights.pluto_weight
                self.pluto_cur.total_conjunct += weights.pluto_weight
                self.pluto_cur.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff_cur - 60) < 5:
                weights.pluto_weight = 5 - (abs(self.planet_aspects[j].pluto_diff_cur - 60))
                weights.pluto_aspect_type = 1
                weights.total_aspect += weights.pluto_weight
                weights.total_sextile += weights.pluto_weight
                weights.total_good += weights.pluto_weight
                self.pluto_cur.weight = 10 - abs(self.planet_aspects[j].pluto_diff_cur - 60)
                self.pluto_cur.aspect_type = 1
                self.pluto_cur.total_aspect += weights.pluto_weight
                self.pluto_cur.total_sextile += weights.pluto_weight
                self.pluto_cur.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff_cur - 90) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff_cur - 90))) * -1
                weights.pluto_aspect_type = 2
                weights.total_aspect += weights.pluto_weight
                weights.total_square += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
                self.pluto_cur.weight = 10 - abs(self.planet_aspects[j].pluto_diff_cur - 90) * -1
                self.pluto_cur.aspect_type = 2
                self.pluto_cur.total_aspect += weights.pluto_weight
                self.pluto_cur.total_square += weights.pluto_weight
                self.pluto_cur.total_bad += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff_cur - 120) < 10:
                weights.pluto_weight = 10 - (abs(self.planet_aspects[j].pluto_diff_cur - 120))
                weights.pluto_aspect_type = 3
                weights.total_aspect += weights.pluto_weight
                weights.total_trine += weights.pluto_weight
                weights.total_good += weights.pluto_weight
                self.pluto_cur.weight = 10 - abs(self.planet_aspects[j].pluto_diff_cur - 120)
                self.pluto_cur.aspect_type = 3
                self.pluto_cur.total_aspect += weights.pluto_weight
                self.pluto_cur.total_trine += weights.pluto_weight
                self.pluto_cur.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff_cur - 180) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff_cur - 180))) * -1
                weights.pluto_aspect_type = 4
                weights.total_aspect += weights.pluto_weight
                weights.total_opposite += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
                self.pluto_cur.weight = 10 - abs(self.planet_aspects[j].pluto_diff_cur - 180) * -1
                self.pluto_cur.aspect_type = 4
                self.pluto_cur.total_aspect += weights.pluto_weight
                self.pluto_cur.total_opposite += weights.pluto_weight
                self.pluto_cur.total_bad += weights.pluto_weight
            else:
                weights.pluto_weight = 0
                weights.pluto_aspect_type = 5

            # Aspect to Marker Right
            if abs(self.planet_aspects[j].marker_diff_cur - 0) < 10:
                weights.marker_weight = 10 - (abs(self.planet_aspects[j].marker_diff_cur - 0))
                weights.marker_aspect_type = 0
                weights.marker_aspect += weights.marker_weight
                weights.marker_conjunct += weights.marker_weight
                weights.marker_good += weights.marker_weight
                self.marker_cur.weight = 10 - abs(self.planet_aspects[j].marker_diff_cur - 0)
                self.marker_cur.aspect_type = 0
                self.marker_cur.total_aspect += weights.marker_weight
                self.marker_cur.total_conjunct += weights.marker_weight
                self.marker_cur.total_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 60) < 5:
                weights.marker_weight = 5 - (abs(self.planet_aspects[j].marker_diff_cur - 60))
                weights.marker_aspect_type = 1
                weights.marker_aspect += weights.marker_weight
                weights.marker_sextile += weights.marker_weight
                weights.marker_good += weights.marker_weight
                self.marker_cur.weight = 10 - abs(self.planet_aspects[j].marker_diff_cur - 60)
                self.marker_cur.aspect_type = 1
                self.marker_cur.total_aspect += weights.marker_weight
                self.marker_cur.total_sextile += weights.marker_weight
                self.marker_cur.total_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 90) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff_cur - 90))) * -1
                weights.marker_aspect_type = 2
                weights.marker_aspect += weights.marker_weight
                weights.marker_square += weights.marker_weight
                weights.marker_bad += weights.marker_weight
                self.marker_cur.weight = 10 - abs(self.planet_aspects[j].marker_diff_cur - 90) * -1
                self.marker_cur.aspect_type = 2
                self.marker_cur.total_aspect += weights.marker_weight
                self.marker_cur.total_square += weights.marker_weight
                self.marker_cur.total_bad += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 120) < 10:
                weights.marker_weight = 10 - (abs(self.planet_aspects[j].marker_diff_cur - 120))
                weights.marker_aspect_type = 3
                weights.marker_aspect += weights.marker_weight
                weights.marker_trine += weights.marker_weight
                weights.marker_good += weights.marker_weight
                self.marker_cur.weight = 10 - abs(self.planet_aspects[j].marker_diff_cur - 120)
                self.marker_cur.aspect_type = 3
                self.marker_cur.total_aspect += weights.marker_weight
                self.marker_cur.total_trine += weights.marker_weight
                self.marker_cur.total_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 180) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff_cur - 180))) * -1
                weights.marker_aspect_type = 4
                weights.marker_aspect += weights.marker_weight
                weights.marker_opposite += weights.marker_weight
                weights.marker_bad += weights.marker_weight
                self.marker_cur.weight = 10 - abs(self.planet_aspects[j].marker_diff_cur - 180) * -1
                self.marker_cur.aspect_type = 4
                self.marker_cur.total_aspect += weights.marker_weight
                self.marker_cur.total_opposite += weights.marker_weight
                self.marker_cur.total_bad += weights.marker_weight
            else:
                weights.marker_weight = 0
                weights.marker_aspect_type = 5

            self.current_weight_list.append(weights)

    def _create_planet_info(self):
        """Create natal and current planet information"""
        planet_names = ["Sun", "Moon", "Mercury", "Venus", "Mars",
                       "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]

        self.terry_planet_signs = []
        self.current_planet_signs = []

        for j in range(10):
            # Create natal planet entry
            natal_entry = NatalPlanetStruct()
            house = int(float(self.terry_planets[j + 1]) / 30.0)
            degrees = (float(self.terry_planets[j + 1]) / 30) - house
            house += 1

            natal_entry.name = planet_names[j]
            natal_entry.house = house
            natal_entry.degree = degrees
            natal_entry.sign = int((house * 100) + (degrees * 30))

            self.terry_planet_signs.append(natal_entry.sign)
            self.natal_planets.append(natal_entry)

            # Create current planet entry
            current_entry = CurrentPlanetStruct()
            house = int(float(self.current_planets[j + 1]) / 30)
            degrees = (float(self.current_planets[j + 1]) / 30) - house
            house += 1

            current_entry.name = planet_names[j]
            current_entry.house = house
            current_entry.degree = degrees
            current_entry.sign = int((house * 100) + (degrees * 30))

            self.current_planet_signs.append(current_entry.sign)
            self.current_planets_2.append(current_entry)

    def _create_chakra_list(self):
        """Create chakra list based on houses"""
        chakra_names = [
            "AriesGreen", "TaurusRed", "GeminiIndego", "CancerViolet",
            "LeoYellow", "VirgoOrange", "LibraGreen", "ScorpioIndego",
            "SagittariusViolet", "CapricornYellow", "AquariusBlue", "PiscesOrange"
        ]

        self.chakra_list.clear()

        for house in range(1, 13):
            chakra = ChakraStruct()
            chakra.name = chakra_names[house - 1]

            # Aggregate weight data for this house
            for j in range(10):
                if self.current_planets_2[j].house == house:
                    chakra.current_good += self.current_weight_list[j].total_good
                    chakra.current_bad += self.current_weight_list[j].total_bad
                    chakra.current_total += self.current_weight_list[j].total_aspect

                if self.natal_planets[j].house == house:
                    chakra.natal_good += self.natal_weight_list[j].total_good
                    chakra.natal_bad += self.natal_weight_list[j].total_bad
                    chakra.natal_total += self.natal_weight_list[j].total_aspect

            self.chakra_list.append(chakra)

    def save_file_chakras(self, file_path: str = r"C:/Terry/NVIDIA_Training/First_Project/Data/Results.csv"):
        """Save chakra data to CSV file"""

        with open('C:/Terry/NVIDIA_Training/First_Project/Data/Results.csv', mode='r') as file:
            csvFile = csv.reader(file)
            self.rows = list(csvFile)


        # Current and Natal Planet Positions
        for k in range(11):
            # print("Planet ", k, " Current: ", self.current_planets[k], " Natal: ", self.terry_planets[k])
            self.rows[k+1][1] = self.terry_planets[k]
            self.rows[k+1][5] = self.current_planets[k]
            #self.rows[k+1][5] = self.current_planets[k]
            #self.rows[k+1][5] = self.current_planets[k]

        for k in range(10):
            # print("Planet ", k, " Current: ", self.current_planets[k], " Natal: ", self.terry_planets[k])
            self.rows[k+2][2] = self.natal_planets[k].house
            self.rows[k+2][3] = self.natal_planets[k].degree * 30
            self.rows[k+2][6] = self.current_planets_2[k].house
            self.rows[k+2][7] = self.current_planets_2[k].degree * 30

            #self.rows[k+1][5] = self.current_planets[k]
            #self.rows[k+1][5] = self.current_planets[k]

        self.rows[12][1] = self.left_marker_display
        self.rows[12][5] = self.right_marker_display

        house = int(self.left_marker_display / 30)
        degrees = (self.left_marker_display / 30) - house
        house += 1
        self.rows[12][2] = house
        self.rows[12][3] = degrees * 30

        house = int(self.right_marker_display / 30)
        degrees = (self.right_marker_display / 30) - house
        house += 1
        self.rows[12][6] = house
        self.rows[12][7] = degrees * 30


        # Current Weights - Current vs Natal
        self.range = 11
        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][1] = self.natal_weight_list[k].sun_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][2] = self.natal_weight_list[k].sun_aspect_type
        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][4] = self.natal_weight_list[k].moon_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][5] = self.natal_weight_list[k].moon_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][7] = self.natal_weight_list[k].mercury_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][8] = self.natal_weight_list[k].mercury_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][10] = self.natal_weight_list[k].venus_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][11] = self.natal_weight_list[k].venus_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][13] = self.natal_weight_list[k].mars_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][14] = self.natal_weight_list[k].mars_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][16] = self.natal_weight_list[k].saturn_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][17] = self.natal_weight_list[k].saturn_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][19] = self.natal_weight_list[k].uranus_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][20] = self.natal_weight_list[k].uranus_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][22] = self.natal_weight_list[k].neptune_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][23] = self.natal_weight_list[k].neptune_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][25] = self.natal_weight_list[k].neptune_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][26] = self.natal_weight_list[k].neptune_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][28] = self.natal_weight_list[k].pluto_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][29] = self.natal_weight_list[k].pluto_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][31] = self.natal_weight_list[k].marker_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+14][32] = self.natal_weight_list[k].marker_aspect_type

        # Current Weights - Natal vs Current

        # Current Weights - Current vs Natal
        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][1] = self.current_weight_list[k].sun_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][2] = self.current_weight_list[k].sun_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][4] = self.current_weight_list[k].moon_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][5] = self.current_weight_list[k].moon_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][7] = self.current_weight_list[k].mercury_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][8] = self.current_weight_list[k].mercury_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][10] = self.current_weight_list[k].venus_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][11] = self.current_weight_list[k].venus_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][13] = self.current_weight_list[k].mars_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][14] = self.current_weight_list[k].mars_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][16] = self.current_weight_list[k].saturn_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][17] = self.current_weight_list[k].saturn_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][19] = self.current_weight_list[k].uranus_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][20] = self.current_weight_list[k].uranus_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][22] = self.current_weight_list[k].neptune_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][23] = self.current_weight_list[k].neptune_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][25] = self.current_weight_list[k].neptune_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][26] = self.current_weight_list[k].neptune_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][28] = self.current_weight_list[k].pluto_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][29] = self.current_weight_list[k].pluto_aspect_type

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][31] = self.current_weight_list[k].marker_weight

        for k in range(self.range):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])
            self.rows[k+27][32] = self.current_weight_list[k].marker_aspect_type

        # for k in range(10):
        #     # print("Natal Planet ", k, " : ", self.natal_planets[k])
        #     self.rows[k+40][1] = self.natal_planets[k]

        # for k in range(10):
        #     # print("Terry Planet Signs ", k, " : ", self.terry_planet_signs[k])
        #     self.rows[k+40][2] = self.terry_planet_signs[k]

        # for k in range(10):
        #     # print("Current Planet ", k, " : ", self.current_planets_2[k])
        #     self.rows[k+40][3] = self.current_planets_2[k]

        # for k in range(10):
        #     # print("Current Planet Signs ", k, " : ", self.current_planet_signs[k])
        #     self.rows[k+40][4] = self.current_planet_signs[k]


        # Current Weights - Current vs Natal
        #for k in range(7):
            # print("Natal Weights List ", k, " : ", self.natal_weight_list[k])

        # Natel weights
        self.rows[43][1] = self.sun.total_aspect
        self.rows[43][2] = self.sun.total_good
        self.rows[43][3] = self.sun.total_bad
        self.rows[43][4] = self.sun.total_conjunct
        self.rows[43][5] = self.sun.total_sextile
        self.rows[43][6] = self.sun.total_square
        self.rows[43][7] = self.sun.total_trine
        self.rows[43][8] = self.sun.total_opposite

        self.rows[44][1] = self.moon.total_aspect
        self.rows[44][2] = self.moon.total_good
        self.rows[44][3] = self.moon.total_bad
        self.rows[44][4] = self.moon.total_conjunct
        self.rows[44][5] = self.moon.total_sextile
        self.rows[44][6] = self.moon.total_square
        self.rows[44][7] = self.moon.total_trine
        self.rows[44][8] = self.moon.total_opposite

        self.rows[45][1] = self.mercury.total_aspect
        self.rows[45][2] = self.mercury.total_good
        self.rows[45][3] = self.mercury.total_bad
        self.rows[45][4] = self.mercury.total_conjunct
        self.rows[45][5] = self.mercury.total_sextile
        self.rows[45][6] = self.mercury.total_square
        self.rows[45][7] = self.mercury.total_trine
        self.rows[45][8] = self.mercury.total_opposite

        self.rows[46][1] = self.venus.total_aspect
        self.rows[46][2] = self.venus.total_good
        self.rows[46][3] = self.venus.total_bad
        self.rows[46][4] = self.venus.total_conjunct
        self.rows[46][5] = self.venus.total_sextile
        self.rows[46][6] = self.venus.total_square
        self.rows[46][7] = self.venus.total_trine
        self.rows[46][8] = self.venus.total_opposite

        self.rows[47][1] = self.mars.total_aspect
        self.rows[47][2] = self.mars.total_good
        self.rows[47][3] = self.mars.total_bad
        self.rows[47][4] = self.mars.total_conjunct
        self.rows[47][5] = self.mars.total_sextile
        self.rows[47][6] = self.mars.total_square
        self.rows[47][7] = self.mars.total_trine
        self.rows[47][8] = self.mars.total_opposite

        self.rows[48][1] = self.jupiter.total_aspect
        self.rows[48][2] = self.jupiter.total_good
        self.rows[48][3] = self.jupiter.total_bad
        self.rows[48][4] = self.jupiter.total_conjunct
        self.rows[48][5] = self.jupiter.total_sextile
        self.rows[48][6] = self.jupiter.total_square
        self.rows[48][7] = self.jupiter.total_trine
        self.rows[48][8] = self.jupiter.total_opposite

        self.rows[49][1] = self.saturn.total_aspect
        self.rows[49][2] = self.saturn.total_good
        self.rows[49][3] = self.saturn.total_bad
        self.rows[49][4] = self.saturn.total_conjunct
        self.rows[49][5] = self.saturn.total_sextile
        self.rows[49][6] = self.saturn.total_square
        self.rows[49][7] = self.saturn.total_trine
        self.rows[49][8] = self.saturn.total_opposite

        self.rows[50][1] = self.uranus.total_aspect
        self.rows[50][2] = self.uranus.total_good
        self.rows[50][3] = self.uranus.total_bad
        self.rows[50][4] = self.uranus.total_conjunct
        self.rows[50][5] = self.uranus.total_sextile
        self.rows[50][6] = self.uranus.total_square
        self.rows[50][7] = self.uranus.total_trine
        self.rows[50][8] = self.uranus.total_opposite

        self.rows[51][1] = self.neptune.total_aspect
        self.rows[51][2] = self.neptune.total_good
        self.rows[51][3] = self.neptune.total_bad
        self.rows[51][4] = self.neptune.total_conjunct
        self.rows[51][5] = self.neptune.total_sextile
        self.rows[51][6] = self.neptune.total_square
        self.rows[51][7] = self.neptune.total_trine
        self.rows[51][8] = self.neptune.total_opposite

        self.rows[52][1] = self.pluto.total_aspect
        self.rows[52][2] = self.pluto.total_good
        self.rows[52][3] = self.pluto.total_bad
        self.rows[52][4] = self.pluto.total_conjunct
        self.rows[52][5] = self.pluto.total_sextile
        self.rows[52][6] = self.pluto.total_square
        self.rows[52][7] = self.pluto.total_trine
        self.rows[52][8] = self.pluto.total_opposite

        self.rows[53][1] = self.marker.total_aspect
        self.rows[53][2] = self.marker.total_good
        self.rows[53][3] = self.marker.total_bad
        self.rows[53][4] = self.marker.total_conjunct
        self.rows[53][5] = self.marker.total_sextile
        self.rows[53][6] = self.marker.total_square
        self.rows[53][7] = self.marker.total_trine
        self.rows[53][8] = self.marker.total_opposite


        # Natel weights
        self.rows[55][1] = self.sun_cur.total_aspect
        self.rows[55][2] = self.sun_cur.total_good
        self.rows[55][3] = self.sun_cur.total_bad
        self.rows[55][4] = self.sun_cur.total_conjunct
        self.rows[55][5] = self.sun_cur.total_sextile
        self.rows[55][6] = self.sun_cur.total_square
        self.rows[55][7] = self.sun_cur.total_trine
        self.rows[55][8] = self.sun_cur.total_opposite

        self.rows[56][1] = self.moon_cur.total_aspect
        self.rows[56][2] = self.moon_cur.total_good
        self.rows[56][3] = self.moon_cur.total_bad
        self.rows[56][4] = self.moon_cur.total_conjunct
        self.rows[56][5] = self.moon_cur.total_sextile
        self.rows[56][6] = self.moon_cur.total_square
        self.rows[56][7] = self.moon_cur.total_trine
        self.rows[56][8] = self.moon_cur.total_opposite

        self.rows[57][1] = self.mercury_cur.total_aspect
        self.rows[57][2] = self.mercury_cur.total_good
        self.rows[57][3] = self.mercury_cur.total_bad
        self.rows[57][4] = self.mercury_cur.total_conjunct
        self.rows[57][5] = self.mercury_cur.total_sextile
        self.rows[57][6] = self.mercury_cur.total_square
        self.rows[57][7] = self.mercury_cur.total_trine
        self.rows[57][8] = self.mercury_cur.total_opposite

        self.rows[58][1] = self.venus_cur.total_aspect
        self.rows[58][2] = self.venus_cur.total_good
        self.rows[58][3] = self.venus_cur.total_bad
        self.rows[58][4] = self.venus_cur.total_conjunct
        self.rows[58][5] = self.venus_cur.total_sextile
        self.rows[58][6] = self.venus_cur.total_square
        self.rows[58][7] = self.venus_cur.total_trine
        self.rows[58][8] = self.venus_cur.total_opposite

        self.rows[59][1] = self.mars_cur.total_aspect
        self.rows[59][2] = self.mars_cur.total_good
        self.rows[59][3] = self.mars_cur.total_bad
        self.rows[59][4] = self.mars_cur.total_conjunct
        self.rows[59][5] = self.mars_cur.total_sextile
        self.rows[59][6] = self.mars_cur.total_square
        self.rows[59][7] = self.mars_cur.total_trine
        self.rows[59][8] = self.mars_cur.total_opposite

        self.rows[60][1] = self.jupiter_cur.total_aspect
        self.rows[60][2] = self.jupiter_cur.total_good
        self.rows[60][3] = self.jupiter_cur.total_bad
        self.rows[60][4] = self.jupiter_cur.total_conjunct
        self.rows[60][5] = self.jupiter_cur.total_sextile
        self.rows[60][6] = self.jupiter_cur.total_square
        self.rows[60][7] = self.jupiter_cur.total_trine
        self.rows[60][8] = self.jupiter_cur.total_opposite

        self.rows[61][1] = self.saturn_cur.total_aspect
        self.rows[61][2] = self.saturn_cur.total_good
        self.rows[61][3] = self.saturn_cur.total_bad
        self.rows[61][4] = self.saturn_cur.total_conjunct
        self.rows[61][5] = self.saturn_cur.total_sextile
        self.rows[61][6] = self.saturn_cur.total_square
        self.rows[61][7] = self.saturn_cur.total_trine
        self.rows[61][8] = self.saturn_cur.total_opposite

        self.rows[62][1] = self.uranus_cur.total_aspect
        self.rows[62][2] = self.uranus_cur.total_good
        self.rows[62][3] = self.uranus_cur.total_bad
        self.rows[62][4] = self.uranus_cur.total_conjunct
        self.rows[62][5] = self.uranus_cur.total_sextile
        self.rows[62][6] = self.uranus_cur.total_square
        self.rows[62][7] = self.uranus_cur.total_trine
        self.rows[62][8] = self.uranus_cur.total_opposite

        self.rows[63][1] = self.neptune_cur.total_aspect
        self.rows[63][2] = self.neptune_cur.total_good
        self.rows[63][3] = self.neptune_cur.total_bad
        self.rows[63][4] = self.neptune_cur.total_conjunct
        self.rows[63][5] = self.neptune_cur.total_sextile
        self.rows[63][6] = self.neptune_cur.total_square
        self.rows[63][7] = self.neptune_cur.total_trine
        self.rows[63][8] = self.neptune_cur.total_opposite

        self.rows[64][1] = self.pluto_cur.total_aspect
        self.rows[64][2] = self.pluto_cur.total_good
        self.rows[64][3] = self.pluto_cur.total_bad
        self.rows[64][4] = self.pluto_cur.total_conjunct
        self.rows[64][5] = self.pluto_cur.total_sextile
        self.rows[64][6] = self.pluto_cur.total_square
        self.rows[64][7] = self.pluto_cur.total_trine
        self.rows[64][8] = self.pluto_cur.total_opposite

        self.rows[65][1] = self.marker_cur.total_aspect
        self.rows[65][2] = self.marker_cur.total_good
        self.rows[65][3] = self.marker_cur.total_bad
        self.rows[65][4] = self.marker_cur.total_conjunct
        self.rows[65][5] = self.marker_cur.total_sextile
        self.rows[65][6] = self.marker_cur.total_square
        self.rows[65][7] = self.marker_cur.total_trine
        self.rows[65][8] = self.marker_cur.total_opposite

        # for k in range(10):
        #     print("Natal Planet ", k, " : ", self.natal_planets[k])
        #     self.rows[k+67][1] = self.natal_planets[k]

        # for k in range(10):
        #     print("Terry Planet Signs ", k, " : ", self.terry_planet_signs[k])
        #     self.rows[k+77][2] = self.terry_planet_signs[k]

        # for k in range(10):
        #     print("Current Planet ", k, " : ", self.current_planets_2[k])
        #     self.rows[k+88][3] = self.current_planets_2[k]

        # for k in range(10):
        #     print("Current Planet Signs ", k, " : ", self.current_planet_signs[k])
        #     self.rows[k+99][4] = self.current_planet_signs[k]

        try:
            with open('C:/Terry/NVIDIA_Training/First_Project/Data/Results.csv', 'w', newline='') as f:
                writer = csv.writer(f)
                #writer.writerow(header)
                writer.writerows(self.rows)
            print(f"Chakra data saved to C:/Terry/NVIDIA_Training/First_Project/Data/Results.csv")
        except IOError as e:
            print(f"Error saving chakra data: {e}")



        # for k in range(11):
        #     print("Planet ", k, " Current: ", self.current_planets[k], " Natal: ", self.terry_planets[k])

        # for k in range(11):
        #    print("Natal Weights List ", k, " : ", self.natal_weight_list[k])

        # for k in range(11):
        #    print("Current Weights List ", k, " : ", self.current_weight_list[k])

        # for k in range(10):
        #     print("Natal Planet ", k, " : ", self.natal_planets[k])

        # for k in range(10):
        #     print("Terry Planet Signs ", k, " : ", self.terry_planet_signs[k])

        # for k in range(10):
        #     print("Current Planet ", k, " : ", self.current_planets_2[k])

        # for k in range(10):
        #     print("Current Planet Signs ", k, " : ", self.current_planet_signs[k])


        # with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', mode='r') as file:
        #     csvFile = csv.reader(file)
        #     self.rows = list(csvFile)
        #     # print(self.rows[5][0])
        #     # print("Read File again < 1: ",self.rows[5][0])
        #     #for lines in csvFile:
        #     #   print(lines)

        # for i in range(1, 80):
        #     self.rows[i][3] = self.Deck_Temp[i]
        #         #print("Card Save Output: ", self.Deck_Temp[i])

        # Data to be written
        # data = [
        #     [self.rows[0][0], self.rows[0][1], self.rows[0][2], self.rows[0][3]],
        #     [self.rows[1][0], self.rows[1][1], self.rows[1][2], self.rows[1][3]],
        #     [self.rows[2][0], self.rows[2][1], self.rows[2][2], self.rows[2][3]],
        #     [self.rows[3][0], self.rows[3][1], self.rows[3][2], self.rows[3][3]],
        #     [self.rows[4][0], self.rows[4][1], self.rows[4][2], self.rows[4][3]],
        #     [self.rows[5][0], self.rows[5][1], self.rows[5][2], self.rows[5][3]],
        #     [self.rows[6][0], self.rows[6][1], self.rows[6][2], self.rows[6][3]],
        #     [self.rows[7][0], self.rows[7][1], self.rows[7][2], self.rows[7][3]],
        #     [self.rows[8][0], self.rows[8][1], self.rows[8][2], self.rows[8][3]],
        #     [self.rows[9][0], self.rows[9][1], self.rows[9][2], self.rows[9][3]],
        #     [self.rows[10][0], self.rows[10][1], self.rows[10][2], self.rows[10][3]],
        #     [self.rows[11][0], self.rows[11][1], self.rows[11][2], self.rows[11][3]],
        #     [self.rows[12][0], self.rows[12][1], self.rows[12][2], self.rows[12][3]],
        #     [self.rows[13][0], self.rows[13][1], self.rows[13][2], self.rows[13][3]],
        #     [self.rows[14][0], self.rows[14][1], self.rows[14][2], self.rows[14][3]],
        #     [self.rows[15][0], self.rows[15][1], self.rows[15][2], self.rows[15][3]],
        #     [self.rows[16][0], self.rows[16][1], self.rows[16][2], self.rows[16][3]],
        #     [self.rows[17][0], self.rows[17][1], self.rows[17][2], self.rows[17][3]],
        #     [self.rows[18][0], self.rows[18][1], self.rows[18][2], self.rows[18][3]],
        #     [self.rows[19][0], self.rows[19][1], self.rows[19][2], self.rows[19][3]],
        #     [self.rows[20][0], self.rows[20][1], self.rows[20][2], self.rows[20][3]],
        #     [self.rows[21][0], self.rows[21][1], self.rows[21][2], self.rows[21][3]],
        #     [self.rows[22][0], self.rows[22][1], self.rows[22][2], self.rows[22][3]],
        #     [self.rows[23][0], self.rows[23][1], self.rows[23][2], self.rows[23][3]],
        #     [self.rows[24][0], self.rows[24][1], self.rows[24][2], self.rows[24][3]],
        #     [self.rows[25][0], self.rows[25][1], self.rows[25][2], self.rows[25][3]],
        #     [self.rows[26][0], self.rows[26][1], self.rows[26][2], self.rows[26][3]],
        #     [self.rows[27][0], self.rows[27][1], self.rows[27][2], self.rows[27][3]],
        #     [self.rows[28][0], self.rows[28][1], self.rows[28][2], self.rows[28][3]],
        #     [self.rows[29][0], self.rows[29][1], self.rows[29][2], self.rows[29][3]],
        #     [self.rows[30][0], self.rows[30][1], self.rows[30][2], self.rows[30][3]],
        #     [self.rows[31][0], self.rows[31][1], self.rows[31][2], self.rows[31][3]],
        #     [self.rows[32][0], self.rows[32][1], self.rows[32][2], self.rows[32][3]],
        #     [self.rows[33][0], self.rows[33][1], self.rows[33][2], self.rows[33][3]],
        #     [self.rows[34][0], self.rows[34][1], self.rows[34][2], self.rows[34][3]],
        #     [self.rows[35][0], self.rows[35][1], self.rows[35][2], self.rows[35][3]],
        #     [self.rows[36][0], self.rows[36][1], self.rows[36][2], self.rows[36][3]],
        #     [self.rows[37][0], self.rows[37][1], self.rows[37][2], self.rows[37][3]],
        #     [self.rows[38][0], self.rows[38][1], self.rows[38][2], self.rows[38][3]],
        #     [self.rows[39][0], self.rows[39][1], self.rows[39][2], self.rows[39][3]],
        #     [self.rows[40][0], self.rows[40][1], self.rows[40][2], self.rows[40][3]],
        #     [self.rows[41][0], self.rows[41][1], self.rows[41][2], self.rows[41][3]],
        #     [self.rows[42][0], self.rows[42][1], self.rows[42][2], self.rows[42][3]],
        #     [self.rows[43][0], self.rows[43][1], self.rows[43][2], self.rows[43][3]],
        #     [self.rows[44][0], self.rows[44][1], self.rows[44][2], self.rows[44][3]],
        #     [self.rows[45][0], self.rows[45][1], self.rows[45][2], self.rows[45][3]],
        #     [self.rows[46][0], self.rows[46][1], self.rows[46][2], self.rows[46][3]],
        #     [self.rows[47][0], self.rows[47][1], self.rows[47][2], self.rows[47][3]],
        #     [self.rows[48][0], self.rows[48][1], self.rows[48][2], self.rows[48][3]],
        #     [self.rows[49][0], self.rows[49][1], self.rows[49][2], self.rows[49][3]],
        #     [self.rows[50][0], self.rows[50][1], self.rows[50][2], self.rows[50][3]],
        #     [self.rows[51][0], self.rows[51][1], self.rows[51][2], self.rows[51][3]],
        #     [self.rows[52][0], self.rows[52][1], self.rows[52][2], self.rows[52][3]],
        #     [self.rows[53][0], self.rows[53][1], self.rows[53][2], self.rows[53][3]],
        #     [self.rows[54][0], self.rows[54][1], self.rows[54][2], self.rows[54][3]],
        #     [self.rows[55][0], self.rows[55][1], self.rows[55][2], self.rows[55][3]],
        #     [self.rows[56][0], self.rows[56][1], self.rows[56][2], self.rows[56][3]],
        #     [self.rows[57][0], self.rows[57][1], self.rows[57][2], self.rows[57][3]],
        #     [self.rows[58][0], self.rows[58][1], self.rows[58][2], self.rows[58][3]],
        #     [self.rows[59][0], self.rows[59][1], self.rows[59][2], self.rows[59][3]],
        #     [self.rows[60][0], self.rows[60][1], self.rows[60][2], self.rows[60][3]],
        #     [self.rows[61][0], self.rows[61][1], self.rows[61][2], self.rows[61][3]],
        #     [self.rows[62][0], self.rows[62][1], self.rows[62][2], self.rows[62][3]],
        #     [self.rows[63][0], self.rows[63][1], self.rows[63][2], self.rows[63][3]],
        #     [self.rows[64][0], self.rows[64][1], self.rows[64][2], self.rows[64][3]],
        #     [self.rows[65][0], self.rows[65][1], self.rows[65][2], self.rows[65][3]],
        #     [self.rows[66][0], self.rows[66][1], self.rows[66][2], self.rows[66][3]],
        #     [self.rows[67][0], self.rows[67][1], self.rows[67][2], self.rows[67][3]],
        #     [self.rows[68][0], self.rows[68][1], self.rows[68][2], self.rows[68][3]],
        #     [self.rows[69][0], self.rows[69][1], self.rows[69][2], self.rows[69][3]],
        #     [self.rows[70][0], self.rows[70][1], self.rows[70][2], self.rows[70][3]],
        #     [self.rows[71][0], self.rows[71][1], self.rows[71][2], self.rows[71][3]],
        #     [self.rows[72][0], self.rows[72][1], self.rows[72][2], self.rows[72][3]],
        #     [self.rows[73][0], self.rows[73][1], self.rows[73][2], self.rows[73][3]],
        #     [self.rows[74][0], self.rows[74][1], self.rows[74][2], self.rows[74][3]],
        #     [self.rows[75][0], self.rows[75][1], self.rows[75][2], self.rows[75][3]],
        #     [self.rows[76][0], self.rows[76][1], self.rows[76][2], self.rows[76][3]],
        #     [self.rows[77][0], self.rows[77][1], self.rows[77][2], self.rows[77][3]],
        #     [self.rows[78][0], self.rows[78][1], self.rows[78][2], self.rows[78][3]],
        #     [self.rows[79][0], self.rows[79][1], self.rows[79][2], self.rows[79][3]]
        #     ]

        # # header = ['name', 'area', 'country_code2', 'country_code3']
        # with open('C:/Terry/NVIDIA_Training/First_Project/Data/Entanglement_Data.csv', 'w', newline='') as f:
        #     writer = csv.writer(f)
        #     #writer.writerow(header)
        #     writer.writerows(data)
        #     #for i in range(0, 80):
        #     #    writer.writerow(rows[i])

# Example usage
if __name__ == "__main__":
    loader = PlanetLoader()
    loader.start()
