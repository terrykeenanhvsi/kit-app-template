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
        self.sun_cur = None
        self.moon_cur = None
        self.venus_cur = None
        self.mercury_cur = None
        self.mars_cur = None
        self.jupiter_cur = None
        self.saturn_cur = None
        self.uranus_cur = None
        self.neptune = None
        self.pluto = None

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

    def start(self):
        """Initialize the PlanetLoader (called on startup)"""
        # Load ephemeris data

        self.load_ephemeris_data()

        # for t in range(length):
        #     if t > 1:
        #         whole = self.rows[t]
        #         dateNoon = self.rows[t][0]
        #         newEntries = whole.split(',')
        #         newEntries_date = dateNoon.split('/')


        # Initialize dates
        self.last = datetime(2010, 1, 2)
        self.noon = datetime(2010, 1, 2)
        self.today = datetime.now()
        self.terry = datetime(1959, 2, 28)
        self.tomorrow = datetime.now() + timedelta(days=1)
        self.yesterday = datetime.now() - timedelta(days=1)
        self.natal_chart = datetime(2000, 2, 28)
        self.default = datetime(1959, 2, 28)

        # Calculate current time
        hour = self.today.hour
        minute = self.today.minute
        second = self.today.second
        time = hour + (minute / 60) + (second / (60 * 60))
        print("Calling self Load:")
        self.load(self.default, 8.667, self.today, time, 0, 0)

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
        for i in range(1,length):
            entries = self.rows[i]

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
                self.current_planets = entries[:11] + [str(marker_left), str(marker_right)]
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

        self.complete = "Load Complete"
        print("Returning done = ")

        for k in range(11):
            print("Planet ", k, " Current: ", self.current_planets[k], " Natal: ", self.terry_planets[k])

        for k in range(11):
           print("Natal Weights List ", k, " : ", self.natal_weight_list[k])

        for k in range(11):
           print("Current Weights List ", k, " : ", self.current_weight_list[k])

        for k in range(10):
            print("Terry Planet Signs ", k, " : ", self.terry_planet_signs[k])

        for k in range(10):
            print("Current Planet Signs ", k, " : ", self.current_planet_signs[k])

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
        for j in range(1, 13):
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
            if planet_diff.pluto_diff > 180:
                planet_diff.pluto_diff = abs(abs(planet_diff.pluto_diff) - 360)

            planet_diff.marker_diff = abs(float(self.terry_planets[j]) - marker_left)
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
            if planet_diff.pluto_diff_cur > 180:
                planet_diff.pluto_diff_cur = abs(abs(planet_diff.pluto_diff_cur) - 360)

            # planet_diff.marker_diff_cur = abs(float(self.current_planets[j]) - self.marker_right)
            # if planet_diff.marker_diff_cur > 180:
            #     planet_diff.marker_diff_cur = abs(abs(planet_diff.marker_diff_cur) - 360)

            self.planet_aspects.append(planet_diff)

    def _calculate_weights(self):
        """Calculate aspect weights"""
        for j in range(12):
            weights = PlanetWeightsStruct()

            # Calculate conjunct, sextile, square, trine, opposite aspects
            if abs(self.planet_aspects[j].sun_diff - 0) < 10:
                weights.sun_weight = 10 - abs(self.planet_aspects[j].sun_diff - 0)
                weights.sun_aspect_type = 0
                weights.total_aspect += weights.sun_weight
                weights.total_conjunct += weights.sun_weight
                weights.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 60) < 5:
                weights.sun_weight = 5 - abs(self.planet_aspects[j].sun_diff - 60)
                weights.sun_aspect_type = 1
                weights.total_aspect += weights.sun_weight
                weights.total_sextile += weights.sun_weight
                weights.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 90) < 10:
                weights.sun_weight = (10 - abs(self.planet_aspects[j].sun_diff - 90)) * -1
                weights.sun_aspect_type = 2
                weights.total_aspect += weights.sun_weight
                weights.total_square += weights.sun_weight
                weights.total_bad += weights.sun_weight
                weights.total_bad += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 120) < 10:
                weights.sun_weight = 10 - abs(self.planet_aspects[j].sun_diff - 120)
                weights.sun_aspect_type = 3
                weights.total_aspect += weights.sun_weight
                weights.total_trine += weights.sun_weight
                weights.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff - 180) < 10:
                weights.sun_weight = (10 - abs(self.planet_aspects[j].sun_diff - 180)) * -1
                weights.sun_aspect_type = 4
                weights.total_aspect += weights.sun_weight
                weights.total_opposite += weights.sun_weight
                weights.total_bad += weights.sun_weight
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
            elif abs(self.planet_aspects[j].moon_diff - 60) < 5:
                weights.moon_weight = 5 - abs(self.planet_aspects[j].moon_diff - 60)
                weights.moon_aspect_type = 1
                weights.total_aspect += weights.moon_weight
                weights.total_sextile += weights.moon_weight
                weights.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 90) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff - 90)) * -1
                weights.moon_aspect_type = 2
                weights.total_aspect += weights.moon_weight
                weights.total_square += weights.moon_weight
                weights.total_bad += weights.moon_weight
                weights.total_bad += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 120) < 10:
                weights.moon_weight = 10 - abs(self.planet_aspects[j].moon_diff - 120)
                weights.moon_aspect_type = 3
                weights.total_aspect += weights.moon_weight
                weights.total_trine += weights.moon_weight
                weights.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 120) < 10:
                weights.moon_weight = 10 - abs(self.planet_aspects[j].moon_diff - 120)
                weights.moon_aspect_type = 3
                weights.total_aspect += weights.moon_weight
                weights.total_trine += weights.moon_weight
                weights.total_good += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 180) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff - 180)) * -1
                weights.moon_aspect_type = 4
                weights.total_aspect += weights.moon_weight
                weights.total_opposite += weights.moon_weight
                weights.total_bad += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 180) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff - 180)) * -1
                weights.moon_aspect_type = 4
                weights.total_aspect += weights.moon_weight
                weights.total_opposite += weights.moon_weight
                weights.total_bad += weights.moon_weight
            elif abs(self.planet_aspects[j].moon_diff - 180) < 10:
                weights.moon_weight = (10 - abs(self.planet_aspects[j].moon_diff - 180)) * -1
                weights.moon_aspect_type = 4
                weights.total_aspect += weights.moon_weight
                weights.total_opposite += weights.moon_weight
                weights.total_bad += weights.moon_weight
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
            elif abs(self.planet_aspects[j].venus_diff - 60) < 5:
                weights.venus_weight = 5 - (abs(self.planet_aspects[j].venus_diff - 60))
                weights.venus_aspect_type = 1
                weights.total_aspect += weights.venus_weight
                weights.total_sextile += weights.venus_weight
                weights.total_good += weights.venus_weight

            elif abs(self.planet_aspects[j].venus_diff - 90) < 10:
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff - 90))) * -1
                weights.venus_aspect_type = 2
                weights.total_aspect += weights.venus_weight
                weights.total_square += weights.venus_weight
                weights.total_bad += weights.venus_weight

            elif abs(self.planet_aspects[j].venus_diff - 120) < 10:
                weights.venus_weight = 10 - (abs(self.planet_aspects[j].venus_diff - 120))
                weights.venus_aspect_type = 3
                weights.total_aspect += weights.venus_weight
                weights.total_trine += weights.venus_weight
                weights.total_good += weights.venus_weight
            elif abs(self.planet_aspects[j].venus_diff - 180) < 10:
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff - 180))) * -1
                weights.venus_aspect_type = 4
                weights.total_aspect += weights.venus_weight
                weights.total_opposite += weights.venus_weight
                weights.total_bad += weights.venus_weight
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
            elif abs(self.planet_aspects[j].mercury_diff - 60) < 5:
                weights.mercury_weight = 5 - (abs(self.planet_aspects[j].mercury_diff - 60))
                weights.mercury_aspect_type = 1
                weights.total_aspect += weights.mercury_weight
                weights.total_sextile += weights.mercury_weight
                weights.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff - 90) < 10:
                weights.mercury_weight = (10 - (abs(self.planet_aspects[j].mercury_diff - 90))) * -1
                weights.mercury_aspect_type = 2
                weights.total_aspect += weights.mercury_weight
                weights.total_square += weights.mercury_weight
                weights.total_bad += weights.mercury_weight
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
            elif abs(self.planet_aspects[j].mars_diff - 60) < 5:
                weights.mars_weight = 5 - (abs(self.planet_aspects[j].mars_diff - 60))
                weights.mars_aspect_type = 1
                weights.total_aspect += weights.mars_weight
                weights.total_sextile += weights.mars_weight
                weights.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff - 90) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff - 90))) * -1
                weights.mars_aspect_type = 2
                weights.total_aspect += weights.mars_weight
                weights.total_square += weights.mars_weight
                weights.total_bad += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff - 120) < 10:
                weights.mars_weight = 10 - (abs(self.planet_aspects[j].mars_diff - 120))
                weights.mars_aspect_type = 3
                weights.total_aspect += weights.mars_weight
                weights.total_trine += weights.mars_weight
                weights.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff - 180) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff - 180))) * -1
                weights.mars_aspect_type = 4
                weights.total_aspect += weights.mars_weight
                weights.total_opposite += weights.mars_weight
                weights.total_bad += weights.mars_weight
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

            elif abs(self.planet_aspects[j].jupiter_diff - 60) < 5:
               weights.jupiter_weight = 5 - (abs(self.planet_aspects[j].jupiter_diff - 60))
               weights.jupiter_aspect_type = 1
               weights.total_aspect += weights.jupiter_weight
               weights.total_sextile += weights.jupiter_weight
               weights.total_good += weights.jupiter_weight

            elif abs(self.planet_aspects[j].jupiter_diff - 90) < 10:
               weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff - 90))) * -1
               weights.jupiter_aspect_type = 2
               weights.total_aspect += weights.jupiter_weight
               weights.total_square += weights.jupiter_weight
               weights.total_bad += weights.jupiter_weight

            elif abs(self.planet_aspects[j].jupiter_diff - 120) < 10:
               weights.jupiter_weight = 10 - (abs(self.planet_aspects[j].jupiter_diff - 120))
               weights.jupiter_aspect_type = 3
               weights.total_aspect += weights.jupiter_weight
               weights.total_trine += weights.jupiter_weight
               weights.total_good += weights.jupiter_weight

            elif abs(self.planet_aspects[j].jupiter_diff - 180) < 10:
               weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff - 180))) * -1
               weights.jupiter_aspect_type = 4
               weights.total_aspect += weights.jupiter_weight
               weights.total_opposite += weights.jupiter_weight
               weights.total_bad += weights.jupiter_weight

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
            elif abs(self.planet_aspects[j].saturn_diff - 60) < 5:
               weights.saturn_weight = 5 - (abs(self.planet_aspects[j].saturn_diff - 60))
               weights.saturn_aspect_type = 1
               weights.total_aspect += weights.saturn_weight
               weights.total_sextile += weights.saturn_weight
               weights.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff - 90) < 10:
               weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff - 90))) * -1
               weights.saturn_aspect_type = 2
               weights.total_aspect += weights.saturn_weight
               weights.total_square += weights.saturn_weight
               weights.total_bad += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff - 120) < 10:
               weights.saturn_weight = 10 - (abs(self.planet_aspects[j].saturn_diff - 120))
               weights.saturn_aspect_type = 3
               weights.total_aspect += weights.saturn_weight
               weights.total_trine += weights.saturn_weight
               weights.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff - 180) < 10:
               weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff - 180))) * -1
               weights.saturn_aspect_type = 4
               weights.total_aspect += weights.saturn_weight
               weights.total_opposite += weights.saturn_weight
               weights.total_bad += weights.saturn_weight
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
            elif abs(self.planet_aspects[j].uranus_diff - 60) < 5:
                weights.uranus_weight = 5 - (abs(self.planet_aspects[j].uranus_diff - 60))
                weights.uranus_aspect_type = 1
                weights.total_aspect += weights.uranus_weight
                weights.total_sextile += weights.uranus_weight
                weights.total_good += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff - 90) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff - 90))) * -1
                weights.uranus_aspect_type = 2
                weights.total_aspect += weights.uranus_weight
                weights.total_square += weights.uranus_weight
                weights.total_bad += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff - 120) < 10:
                weights.uranus_weight = 10 - (abs(self.planet_aspects[j].uranus_diff - 120))
                weights.uranus_aspect_type = 3
                weights.total_aspect += weights.uranus_weight
                weights.total_trine += weights.uranus_weight
                weights.total_good += weights.uranus_weight

            elif abs(self.planet_aspects[j].uranus_diff - 180) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff - 180))) * -1
                weights.uranus_aspect_type = 4
                weights.total_aspect += weights.uranus_weight
                weights.total_opposite += weights.uranus_weight
                weights.total_bad += weights.uranus_weight
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
            elif abs(self.planet_aspects[j].neptune_diff - 60) < 5:
                weights.neptune_weight = 5 - (abs(self.planet_aspects[j].neptune_diff - 60))
                weights.neptune_aspect_type = 1
                weights.total_aspect += weights.neptune_weight
                weights.total_sextile += weights.neptune_weight
                weights.total_good += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff - 90) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff - 90))) * -1
                weights.neptune_aspect_type = 2
                weights.total_aspect += weights.neptune_weight
                weights.total_square += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff - 120) < 10:
                weights.neptune_weight = 10 - (abs(self.planet_aspects[j].neptune_diff - 120))
                weights.neptune_aspect_type = 3
                weights.total_aspect += weights.neptune_weight
                weights.total_trine += weights.neptune_weight
                weights.total_good += weights.neptune_weight

            elif abs(self.planet_aspects[j].neptune_diff - 180) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff - 180))) * -1
                weights.neptune_aspect_type = 4
                weights.total_aspect += weights.neptune_weight
                weights.total_opposite += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
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
            elif abs(self.planet_aspects[j].pluto_diff - 60) < 5:
                weights.pluto_weight = 5 - (abs(self.planet_aspects[j].pluto_diff - 60))
                weights.pluto_aspect_type = 1
                weights.total_aspect += weights.pluto_weight
                weights.total_sextile += weights.pluto_weight
                weights.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff - 90) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff - 90))) * -1
                weights.pluto_aspect_type = 2
                weights.total_aspect += weights.pluto_weight
                weights.total_square += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff - 120) < 10:
                weights.pluto_weight = 10 - (abs(self.planet_aspects[j].pluto_diff - 120))
                weights.pluto_aspect_type = 3
                weights.total_aspect += weights.pluto_weight
                weights.total_trine += weights.pluto_weight
                weights.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff - 180) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff - 180))) * -1
                weights.pluto_aspect_type = 4
                weights.total_aspect += weights.pluto_weight
                weights.total_opposite += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
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
            elif abs(self.planet_aspects[j].marker_diff - 60) < 5:
                weights.marker_weight = 5 - (abs(self.planet_aspects[j].marker_diff - 60))
                weights.marker_aspect_type = 1
                weights.marker_aspect += weights.marker_weight
                weights.marker_sextile += weights.marker_weight
                weights.marker_good += weights.marker_weight

            elif abs(self.planet_aspects[j].marker_diff - 90) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff - 90))) * -1
                weights.marker_aspect_type = 2
                weights.marker_aspect += weights.marker_weight
                weights.marker_square += weights.marker_weight
                weights.marker_bad += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff - 120) < 10:
                weights.marker_weight = 10 - (abs(self.planet_aspects[j].marker_diff - 120))
                weights.marker_aspect_type = 3
                weights.marker_aspect += weights.marker_weight
                weights.marker_trine += weights.marker_weight
                weights.marker_good += weights.marker_weight

            elif abs(self.planet_aspects[j].marker_diff - 180) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff - 180))) * -1
                weights.marker_aspect_type = 4
                weights.marker_aspect += weights.marker_weight
                weights.marker_opposite += weights.marker_weight
                weights.marker_bad += weights.marker_weight

            else:
                weights.marker_weight = 0
                weights.marker_aspect_type = 5

            self.natal_weight_list.append(weights)

            weights = PlanetWeightsStruct()

            # Aspect to Current Sun
            if abs(self.planet_aspects[j].sun_diff_cur - 0) < 10:
                weights.sun_weight = 10 - (abs(self.planet_aspects[j].sun_diff_cur - 0))
                weights.sun_aspect_type = 0
                weights.total_aspect += weights.sun_weight
                weights.total_conjunct += weights.sun_weight
                weights.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 60) < 5:
                weights.sun_weight = 5 - (abs(self.planet_aspects[j].sun_diff_cur - 60))
                weights.sun_aspect_type = 1
                weights.total_aspect += weights.sun_weight
                weights.total_sextile += weights.sun_weight
                weights.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 90) < 10:
                weights.sun_weight = (10 - (abs(self.planet_aspects[j].sun_diff_cur - 90))) * -1
                weights.sun_aspect_type = 2
                weights.total_aspect += weights.sun_weight
                weights.total_square += weights.sun_weight
                weights.total_bad += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 120) < 10:
                weights.sun_weight = 10 - (abs(self.planet_aspects[j].sun_diff_cur - 120))
                weights.sun_aspect_type = 3
                weights.total_aspect += weights.sun_weight
                weights.total_trine += weights.sun_weight
                weights.total_good += weights.sun_weight
            elif abs(self.planet_aspects[j].sun_diff_cur - 180) < 10:
                weights.sun_weight = (10 - (abs(self.planet_aspects[j].sun_diff_cur - 180))) * -1
                weights.sun_aspect_type = 4
                weights.total_aspect += weights.sun_weight
                weights.total_opposite += weights.sun_weight
                weights.total_bad += weights.sun_weight
            else:
                weights.sun_weight = 0
                weights.sun_aspect_type = 5

            # Aspect to Current Moon
            if (abs(self.planet_aspects[j].moon_diff_cur - 0) < 10):
                weights.moon_weight = 10 - (abs(self.planet_aspects[j].moon_diff_cur - 0))
                weights.moon_aspect_type = 0
                weights.total_aspect += weights.moon_weight
                weights.total_conjunct += weights.moon_weight
                weights.total_good += weights.moon_weight
            elif (abs(self.planet_aspects[j].moon_diff_cur - 60) < 5):
                weights.moon_weight = 5 - (abs(self.planet_aspects[j].moon_diff_cur - 60))
                weights.moon_aspect_type = 1
                weights.total_aspect += weights.moon_weight
                weights.total_sextile += weights.moon_weight
                weights.total_good += weights.moon_weight
            elif (abs(self.planet_aspects[j].moon_diff_cur - 90) < 10):
                weights.moon_weight = (10 - (abs(self.planet_aspects[j].moon_diff_cur - 90))) * -1
                weights.moon_aspect_type = 2
                weights.total_aspect += weights.moon_weight
                weights.total_square += weights.moon_weight
                weights.total_bad += weights.moon_weight
            elif (abs(self.planet_aspects[j].moon_diff_cur - 120) < 10):
                weights.moon_weight = 10 - (abs(self.planet_aspects[j].moon_diff_cur - 120))
                weights.moon_aspect_type = 3
                weights.total_aspect += weights.moon_weight
                weights.total_trine += weights.moon_weight
                weights.total_good += weights.moon_weight
            elif (abs(self.planet_aspects[j].moon_diff_cur - 180) < 10):
                weights.moon_weight = (10 - (abs(self.planet_aspects[j].moon_diff_cur - 180))) * -1
                weights.moon_aspect_type = 4
                weights.total_aspect += weights.moon_weight
                weights.total_opposite += weights.moon_weight
                weights.total_bad += weights.moon_weight
            else:
                weights.moon_weight = 0
                weights.moon_aspect_type = 5

            # Aspect to Current Venus
            if (abs(self.planet_aspects[j].venus_diff_cur - 0) < 10):
                weights.venus_weight = 10 - (abs(self.planet_aspects[j].venus_diff_cur - 0))
                weights.venus_aspect_type = 0
                weights.total_aspect += weights.venus_weight
                weights.total_conjunct += weights.venus_weight
                weights.total_good += weights.venus_weight
            elif (abs(self.planet_aspects[j].venus_diff_cur - 60) < 5):
                weights.venus_weight = 5 - (abs(self.planet_aspects[j].venus_diff_cur - 60))
                weights.venus_aspect_type = 1
                weights.total_aspect += weights.venus_weight
                weights.total_sextile += weights.venus_weight
                weights.total_good += weights.venus_weight
            elif (abs(self.planet_aspects[j].venus_diff_cur - 90) < 10):
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff_cur - 90))) * -1
                weights.venus_aspect_type = 2
                weights.total_aspect += weights.venus_weight
                weights.total_square += weights.venus_weight
                weights.total_bad += weights.venus_weight
            elif (abs(self.planet_aspects[j].venus_diff_cur - 120) < 10):
                weights.venus_weight = 10 - (abs(self.planet_aspects[j].venus_diff_cur - 120))
                weights.venus_aspect_type = 3
                weights.total_aspect += weights.venus_weight
                weights.total_trine += weights.venus_weight
                weights.total_good += weights.venus_weight
            elif (abs(self.planet_aspects[j].venus_diff_cur - 180) < 10):
                weights.venus_weight = (10 - (abs(self.planet_aspects[j].venus_diff_cur - 180))) * -1
                weights.venus_aspect_type = 4
                weights.total_aspect += weights.venus_weight
                weights.total_opposite += weights.venus_weight
                weights.total_bad += weights.venus_weight
            else:
                weights.venus_weight = 0
                weights.venus_aspect_type = 5

            # Aspect to Current Mercury
            if (abs(self.planet_aspects[j].mercury_diff_cur - 0) < 10):
                weights.mercury_weight = 10 - (abs(self.planet_aspects[j].mercury_diff_cur - 0))
                weights.mercury_aspect_type = 0
                weights.total_aspect += weights.mercury_weight
                weights.total_conjunct += weights.mercury_weight
                weights.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 60) < 5:
                weights.mercury_weight = 5 - (abs(self.planet_aspects[j].mercury_diff_cur - 60))
                weights.mercury_aspect_type = 1
                weights.total_aspect += weights.mercury_weight
                weights.total_sextile += weights.mercury_weight
                weights.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 90) < 10:
                weights.mercury_weight = (10 - (abs(self.planet_aspects[j].mercury_diff_cur - 90))) * -1
                weights.mercury_aspect_type = 2
                weights.total_aspect += weights.mercury_weight
                weights.total_square += weights.mercury_weight
                weights.total_bad += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 120) < 10:
                weights.mercury_weight = 10 - (abs(self.planet_aspects[j].mercury_diff_cur - 120))
                weights.mercury_aspect_type = 3
                weights.total_aspect += weights.mercury_weight
                weights.total_trine += weights.mercury_weight
                weights.total_good += weights.mercury_weight
            elif abs(self.planet_aspects[j].mercury_diff_cur - 180) < 10:
                weights.mercury_weight = (10 - (abs(self.planet_aspects[j].mercury_diff_cur - 180))) * -1
                weights.mercury_aspect_type = 4
                weights.total_aspect += weights.mercury_weight
                weights.total_opposite += weights.mercury_weight
                weights.total_bad += weights.mercury_weight
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

            elif abs(self.planet_aspects[j].mars_diff_cur - 60) < 5:
                weights.mars_weight = 5 - (abs(self.planet_aspects[j].mars_diff_cur - 60))
                weights.mars_aspect_type = 1
                weights.total_aspect += weights.mars_weight
                weights.total_sextile += weights.mars_weight
                weights.total_good += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff_cur - 90) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff_cur - 90))) * -1
                weights.mars_aspect_type = 2
                weights.total_aspect += weights.mars_weight
                weights.total_square += weights.mars_weight
                weights.total_bad += weights.mars_weight
            elif abs(self.planet_aspects[j].mars_diff_cur - 120) < 10:
                weights.mars_weight = 10 - (abs(self.planet_aspects[j].mars_diff_cur - 120))
                weights.mars_aspect_type = 3
                weights.total_aspect += weights.mars_weight
                weights.total_trine += weights.mars_weight
                weights.total_good += weights.mars_weight

            elif abs(self.planet_aspects[j].mars_diff_cur - 180) < 10:
                weights.mars_weight = (10 - (abs(self.planet_aspects[j].mars_diff_cur - 180))) * -1
                weights.mars_aspect_type = 4
                weights.total_aspect += weights.mars_weight
                weights.total_opposite += weights.mars_weight
                weights.total_bad += weights.mars_weight
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
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 60) < 5:
                weights.jupiter_weight = 5 - (abs(self.planet_aspects[j].jupiter_diff_cur - 60))
                weights.jupiter_aspect_type = 1
                weights.total_aspect += weights.jupiter_weight
                weights.total_sextile += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 90) < 10:
                weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff_cur - 90))) * -1
                weights.jupiter_aspect_type = 2
                weights.total_aspect += weights.jupiter_weight
                weights.total_square += weights.jupiter_weight
                weights.total_bad += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 120) < 10:
                weights.jupiter_weight = 10 - (abs(self.planet_aspects[j].jupiter_diff_cur - 120))
                weights.jupiter_aspect_type = 3
                weights.total_aspect += weights.jupiter_weight
                weights.total_trine += weights.jupiter_weight
                weights.total_good += weights.jupiter_weight
            elif abs(self.planet_aspects[j].jupiter_diff_cur - 180) < 10:
                weights.jupiter_weight = (10 - (abs(self.planet_aspects[j].jupiter_diff_cur - 180))) * -1
                weights.jupiter_aspect_type = 4
                weights.total_aspect += weights.jupiter_weight
                weights.total_opposite += weights.jupiter_weight
                weights.total_bad += weights.jupiter_weight
            else:
                weights.jupiter_weight = 0
                weights.jupiter_aspect_type = 5

            # Aspect to Current Saturn
            if (abs(self.planet_aspects[j].saturn_diff_cur - 0) < 10):
                weights.saturn_weight = 10 - (abs(self.planet_aspects[j].saturn_diff_cur - 0))
                weights.saturn_aspect_type = 0
                weights.total_aspect += weights.saturn_weight
                weights.total_conjunct += weights.saturn_weight
                weights.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 60) < 5:
                weights.saturn_weight = 5 - (abs(self.planet_aspects[j].saturn_diff_cur - 60))
                weights.saturn_aspect_type = 1
                weights.total_aspect += weights.saturn_weight
                weights.total_sextile += weights.saturn_weight
                weights.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 90) < 10:
                weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff_cur - 90))) * -1
                weights.saturn_aspect_type = 2
                weights.total_aspect += weights.saturn_weight
                weights.total_square += weights.saturn_weight
                weights.total_bad += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 120) < 10:
                weights.saturn_weight = 10 - (abs(self.planet_aspects[j].saturn_diff_cur - 120))
                weights.saturn_aspect_type = 3
                weights.total_aspect += weights.saturn_weight
                weights.total_trine += weights.saturn_weight
                weights.total_good += weights.saturn_weight
            elif abs(self.planet_aspects[j].saturn_diff_cur - 180) < 10:
                weights.saturn_weight = (10 - (abs(self.planet_aspects[j].saturn_diff_cur - 180))) * -1
                weights.saturn_aspect_type = 4
                weights.total_aspect += weights.saturn_weight
                weights.total_opposite += weights.saturn_weight
                weights.total_bad += weights.saturn_weight
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
            elif abs(self.planet_aspects[j].uranus_diff_cur - 60) < 5:
                weights.uranus_weight = 5 - (abs(self.planet_aspects[j].uranus_diff_cur - 60))
                weights.uranus_aspect_type = 1
                weights.total_aspect += weights.uranus_weight
                weights.total_sextile += weights.uranus_weight
                weights.total_good += weights.uranus_weight
            elif abs(self.planet_aspects[j].uranus_diff_cur - 90) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff_cur - 90))) * -1
                weights.uranus_aspect_type = 2
                weights.total_aspect += weights.uranus_weight
                weights.total_square += weights.uranus_weight
                weights.total_bad += weights.uranus_weight
            elif abs(self.planet_aspects[j].uranus_diff_cur - 120) < 10:
                weights.uranus_weight = 10 - (abs(self.planet_aspects[j].uranus_diff_cur - 120))
                weights.uranus_aspect_type = 3
                weights.total_aspect += weights.uranus_weight
                weights.total_trine += weights.uranus_weight
                weights.total_good += weights.uranus_weight
            elif abs(self.planet_aspects[j].uranus_diff_cur - 180) < 10:
                weights.uranus_weight = (10 - (abs(self.planet_aspects[j].uranus_diff_cur - 180))) * -1
                weights.uranus_aspect_type = 4
                weights.total_aspect += weights.uranus_weight
                weights.total_opposite += weights.uranus_weight
                weights.total_bad += weights.uranus_weight
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
            elif abs(self.planet_aspects[j].neptune_diff_cur - 60) < 5:
                weights.neptune_weight = 5 - (abs(self.planet_aspects[j].neptune_diff_cur - 60))
                weights.neptune_aspect_type = 1
                weights.total_aspect += weights.neptune_weight
                weights.total_sextile += weights.neptune_weight
                weights.total_good += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff_cur - 90) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff_cur - 90))) * -1
                weights.neptune_aspect_type = 2
                weights.total_aspect += weights.neptune_weight
                weights.total_square += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff_cur - 120) < 10:
                weights.neptune_weight = 10 - (abs(self.planet_aspects[j].neptune_diff_cur - 120))
                weights.neptune_aspect_type = 3
                weights.total_aspect += weights.neptune_weight
                weights.total_trine += weights.neptune_weight
                weights.total_good += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff_cur - 180) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff_cur - 180))) * -1
                weights.neptune_aspect_type = 4
                weights.total_aspect += weights.neptune_weight
                weights.total_opposite += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
            elif abs(self.planet_aspects[j].neptune_diff_cur - 180) < 10:
                weights.neptune_weight = (10 - (abs(self.planet_aspects[j].neptune_diff_cur - 180))) * -1
                weights.neptune_aspect_type = 4
                weights.total_aspect += weights.neptune_weight
                weights.total_opposite += weights.neptune_weight
                weights.total_bad += weights.neptune_weight
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
            elif abs(self.planet_aspects[j].pluto_diff_cur - 60) < 5:
                weights.pluto_weight = 5 - (abs(self.planet_aspects[j].pluto_diff_cur - 60))
                weights.pluto_aspect_type = 1
                weights.total_aspect += weights.pluto_weight
                weights.total_sextile += weights.pluto_weight
                weights.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff_cur - 90) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff_cur - 90))) * -1
                weights.pluto_aspect_type = 2
                weights.total_aspect += weights.pluto_weight
                weights.total_square += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff_cur - 120) < 10:
                weights.pluto_weight = 10 - (abs(self.planet_aspects[j].pluto_diff_cur - 120))
                weights.pluto_aspect_type = 3
                weights.total_aspect += weights.pluto_weight
                weights.total_trine += weights.pluto_weight
                weights.total_good += weights.pluto_weight
            elif abs(self.planet_aspects[j].pluto_diff_cur - 180) < 10:
                weights.pluto_weight = (10 - (abs(self.planet_aspects[j].pluto_diff_cur - 180))) * -1
                weights.pluto_aspect_type = 4
                weights.total_aspect += weights.pluto_weight
                weights.total_opposite += weights.pluto_weight
                weights.total_bad += weights.pluto_weight
            else:
                weights.pluto_weight = 0
                weights.pluto_aspect_type = 5

            # Aspect to Marker Left
            if abs(self.planet_aspects[j].marker_diff_cur - 0) < 10:
                weights.marker_weight = 10 - (abs(self.planet_aspects[j].marker_diff_cur - 0))
                weights.marker_aspect_type = 0
                weights.marker_aspect += weights.marker_weight
                weights.marker_conjunct += weights.marker_weight
                weights.marker_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 60) < 5:
                weights.marker_weight = 5 - (abs(self.planet_aspects[j].marker_diff_cur - 60))
                weights.marker_aspect_type = 1
                weights.marker_aspect += weights.marker_weight
                weights.marker_sextile += weights.marker_weight
                weights.marker_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 90) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff_cur - 90))) * -1
                weights.marker_aspect_type = 2
                weights.marker_aspect += weights.marker_weight
                weights.marker_square += weights.marker_weight
                weights.marker_bad += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 120) < 10:
                weights.marker_weight = 10 - (abs(self.planet_aspects[j].marker_diff_cur - 120))
                weights.marker_aspect_type = 3
                weights.marker_aspect += weights.marker_weight
                weights.marker_trine += weights.marker_weight
                weights.marker_good += weights.marker_weight
            elif abs(self.planet_aspects[j].marker_diff_cur - 180) < 10:
                weights.marker_weight = (10 - (abs(self.planet_aspects[j].marker_diff_cur - 180))) * -1
                weights.marker_aspect_type = 4
                weights.marker_aspect += weights.marker_weight
                weights.marker_opposite += weights.marker_weight
                weights.marker_bad += weights.marker_weight
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
            # print("chakra_list house loop = ", house)

            # Aggregate weight data for this house
            for j in range(10):
                # print("weight j loop = ", j)
                if self.current_planets_2[j].house == house:
                    chakra.current_good += self.current_weight_list[j].total_good
                    chakra.current_bad += self.current_weight_list[j].total_bad
                    chakra.current_total += self.current_weight_list[j].total_aspect
                    chakra.current_conjunct += self.current_weight_list[j].total_conjunct
                    chakra.current_opposite += self.current_weight_list[j].total_opposite
                    chakra.current_sextile += self.current_weight_list[j].total_sextile
                    chakra.current_square += self.current_weight_list[j].total_square
                    chakra.current_trine += self.current_weight_list[j].total_trine

                if self.natal_planets[j].house == house:
                    chakra.natal_good += self.natal_weight_list[j].total_good
                    chakra.natal_bad += self.natal_weight_list[j].total_bad
                    chakra.natal_total += self.natal_weight_list[j].total_aspect
                    chakra.natal_conjunct += self.natal_weight_list[j].total_conjunct
                    chakra.natal_opposite += self.natal_weight_list[j].total_opposite
                    chakra.natal_sextile += self.natal_weight_list[j].total_sextile
                    chakra.natal_square += self.natal_weight_list[j].total_square
                    chakra.natal_trine += self.natal_weight_list[j].total_trine

            self.chakra_list.append(chakra)

    def save_file_chakras(self, file_path: str = r"C:\MatrixEnd\Entanglement_Tarot\Chakras.csv"):
        """Save chakra data to CSV file"""
        csv_row = f"{self.left_side_display},{self.left_time_display}," \
                  f"{self.right_side_display},{self.right_time_display},"

        # Add chakra totals
        for j in range(12):
            csv_row += f"{self.chakra_list[j].total_aspect:.2f},"

        # Add natal weights
        for j in range(12):
            csv_row += f"{self.natal_weight_list[j].total_aspect:.2f},"

        # Add current weights
        for j in range(12):
            csv_row += f"{self.current_weight_list[j].total_aspect:.2f},"

        try:
            with open(file_path, 'a') as f:
                f.write(csv_row + '\n')
            print(f"Chakra data saved to {file_path}")
        except IOError as e:
            print(f"Error saving chakra data: {e}")


# Example usage
if __name__ == "__main__":
    loader = PlanetLoader()
    loader.start()
