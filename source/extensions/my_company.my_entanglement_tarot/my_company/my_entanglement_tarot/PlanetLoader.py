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

            if self.noon.date() == left_side.date():
                self.left_noon_planets = entries
                print("self.left_noon_planets = ", self.left_noon_planets)

            if self.noon.date() == (left_side + timedelta(days=1)).date():
                self.left_tomorrow_planets = entries
                print("self.left_tomorrow_planets = ", self.left_tomorrow_planets)

            if self.noon.date() == (left_side - timedelta(days=1)).date():
                self.left_yesterday_planets = entries
                print("self.left_yesterday_planets = ", self.left_yesterday_planets)





        # i = 0

        # for line in self.ephemeris_txt:
        #     if not line.strip():
        #         continue

        #     entries = line.split(',')
        #     entries_date = entries[0].split('/')

        #     # Format date components
        #     if len(entries_date[0]) < 2:
        #         entries_date[0] = "0" + entries_date[0]

        #     if len(entries_date) > 1:
        #         if len(entries_date[1]) < 2:
        #             entries_date[1] = "0" + entries_date[1]

        #         if i < 36162:
        #             entries_date[2] = "19" + entries_date[2]
        #         else:
        #             entries_date[2] = "20" + entries_date[2]

        #         noon_str = f"{entries_date[0]}/{entries_date[1]}/{entries_date[2]}"
        #         self.noon = datetime.strptime(noon_str, "%m/%d/%Y")

        #         # Check for matching dates
        #         if self.noon.date() == right_side.date():
        #             self.noon_planets = entries
        #             self.current_planets_entries = entries
        #             self.current_planets = entries[:11] + [str(marker_left), str(marker_right)]

        #         if self.noon.date() == (right_side + timedelta(days=1)).date():
        #             self.right_tomorrow_planets = entries

        #         if self.noon.date() == (right_side - timedelta(days=1)).date():
        #             self.right_yesterday_planets = entries

        #         if self.noon.date() == self.natal_chart.date():
        #             self.terry_planets_entries = entries
        #             self.terry_planets = entries[:11] + [str(marker_left), str(marker_right)]

        #         if self.noon.date() == left_side.date():
        #             self.left_noon_planets = entries

        #         if self.noon.date() == (left_side + timedelta(days=1)).date():
        #             self.left_tomorrow_planets = entries

        #         if self.noon.date() == (left_side - timedelta(days=1)).date():
        #             self.left_yesterday_planets = entries

        #   i += 1

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

            # Continue for other planets...
            # (Abbreviated for space, but would continue pattern)

            planet_diff.marker_diff = abs(float(self.terry_planets[j]) - marker_left)
            if planet_diff.marker_diff > 180:
                planet_diff.marker_diff = abs(abs(planet_diff.marker_diff) - 360)

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
            if abs(self.planet_aspects[j].VenusDiff - 0) < 10:
                weights.VenusWeight = 10 - (abs(self.planet_aspects[j].VenusDiff - 0))
                weights.VenusAspectType = 0
                weights.TotalAspect += weights.VenusWeight
                weights.TotalConjunct += weights.VenusWeight
                weights.TotalGood += weights.VenusWeight
            elif abs(self.planet_aspects[j].VenusDiff - 60) < 5:
                weights.VenusWeight = 5 - (abs(self.planet_aspects[j].VenusDiff - 60))
                weights.VenusAspectType = 1
                weights.TotalAspect += weights.VenusWeight
                weights.TotalSextile += weights.VenusWeight
                weights.TotalGood += weights.VenusWeight

            elif abs(self.planet_aspects[j].VenusDiff - 90) < 10:
                weights.VenusWeight = (10 - (abs(self.planet_aspects[j].VenusDiff - 90))) * -1
                weights.VenusAspectType = 2
                weights.TotalAspect += weights.VenusWeight
                weights.TotalSquare += weights.VenusWeight
                weights.TotalBad += weights.VenusWeight

            elif abs(self.planet_aspects[j].VenusDiff - 120) < 10:
                weights.VenusWeight = 10 - (abs(self.planet_aspects[j].VenusDiff - 120))
                weights.VenusAspectType = 3
                weights.TotalAspect += weights.VenusWeight
                weights.TotalTrine += weights.VenusWeight
                weights.TotalGood += weights.VenusWeight
            elif abs(self.planet_aspects[j].VenusDiff - 180) < 10:
                weights.VenusWeight = (10 - (abs(self.planet_aspects[j].VenusDiff - 180))) * -1
                weights.VenusAspectType = 4
                weights.TotalAspect += weights.VenusWeight
                weights.TotalOpposite += weights.VenusWeight
                weights.TotalBad += weights.VenusWeight
            else:
                weights.VenusWeight = 0
                weights.VenusAspectType = 5

            # Aspect to Current Mercury
            if abs(self.planet_aspects[j].MercuryDiff - 0) < 10:
                weights.MercuryWeight = 10 - (abs(self.planet_aspects[j].MercuryDiff - 0))
                weights.MercuryAspectType = 0
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalConjunct += weights.MercuryWeight
                weights.TotalGood += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff - 60) < 5:
                weights.MercuryWeight = 5 - (abs(self.planet_aspects[j].MercuryDiff - 60))
                weights.MercuryAspectType = 1
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalSextile += weights.MercuryWeight
                weights.TotalGood += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff - 90) < 10:
                weights.MercuryWeight = (10 - (abs(self.planet_aspects[j].MercuryDiff - 90))) * -1
                weights.MercuryAspectType = 2
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalSquare += weights.MercuryWeight
                weights.TotalBad += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff - 120) < 10:
                weights.MercuryWeight = 10 - (abs(self.planet_aspects[j].MercuryDiff - 120))
                weights.MercuryAspectType = 3
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalTrine += weights.MercuryWeight
                weights.TotalGood += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff - 180) < 10:
                weights.MercuryWeight = (10 - (abs(self.planet_aspects[j].MercuryDiff - 180))) * -1
                weights.MercuryAspectType = 4
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalOpposite += weights.MercuryWeight
                weights.TotalBad += weights.MercuryWeight
            else:
                weights.MercuryWeight = 0
                weights.MercuryAspectType = 5


            # Aspect to Current Mars
            if abs(self.planet_aspects[j].MarsDiff - 0) < 10:
                weights.MarsWeight = 10 - (abs(self.planet_aspects[j].MarsDiff - 0))
                weights.MarsAspectType = 0
                weights.TotalAspect += weights.MarsWeight
                weights.TotalConjunct += weights.MarsWeight
                weights.TotalGood += weights.MarsWeight
            elif abs(self.planet_aspects[j].MarsDiff - 60) < 5:
                weights.MarsWeight = 5 - (abs(self.planet_aspects[j].MarsDiff - 60))
                weights.MarsAspectType = 1
                weights.TotalAspect += weights.MarsWeight
                weights.TotalSextile += weights.MarsWeight
                weights.TotalGood += weights.MarsWeight
            elif abs(self.planet_aspects[j].MarsDiff - 90) < 10:
                weights.MarsWeight = (10 - (abs(self.planet_aspects[j].MarsDiff - 90))) * -1
                weights.MarsAspectType = 2
                weights.TotalAspect += weights.MarsWeight
                weights.TotalSquare += weights.MarsWeight
                weights.TotalBad += weights.MarsWeight
            elif abs(self.planet_aspects[j].MarsDiff - 120) < 10:
                weights.MarsWeight = 10 - (abs(self.planet_aspects[j].MarsDiff - 120))
                weights.MarsAspectType = 3
                weights.TotalAspect += weights.MarsWeight
                weights.TotalTrine += weights.MarsWeight
                weights.TotalGood += weights.MarsWeight
            elif abs(self.planet_aspects[j].MarsDiff - 180) < 10:
                weights.MarsWeight = (10 - (abs(self.planet_aspects[j].MarsDiff - 180))) * -1
                weights.MarsAspectType = 4
                weights.TotalAspect += weights.MarsWeight
                weights.TotalOpposite += weights.MarsWeight
                weights.TotalBad += weights.MarsWeight
            else:
                weights.MarsWeight = 0
                weights.MarsAspectType = 5

            # Aspect to Current Jupiter
            if abs(self.planet_aspects[j].JupiterDiff - 0) < 10:
               weights.JupiterWeight = 10 - (abs(self.planet_aspects[j].JupiterDiff - 0))
               weights.JupiterAspectType = 0
               weights.TotalAspect += weights.JupiterWeight
               weights.TotalConjunct += weights.JupiterWeight
               weights.TotalGood += weights.JupiterWeight

            elif abs(self.planet_aspects[j].JupiterDiff - 60) < 5:
               weights.JupiterWeight = 5 - (abs(self.planet_aspects[j].JupiterDiff - 60))
               weights.JupiterAspectType = 1
               weights.TotalAspect += weights.JupiterWeight
               weights.TotalSextile += weights.JupiterWeight
               weights.TotalGood += weights.JupiterWeight

            elif abs(self.planet_aspects[j].JupiterDiff - 90) < 10:
               weights.JupiterWeight = (10 - (abs(self.planet_aspects[j].JupiterDiff - 90))) * -1
               weights.JupiterAspectType = 2
               weights.TotalAspect += weights.JupiterWeight
               weights.TotalSquare += weights.JupiterWeight
               weights.TotalBad += weights.JupiterWeight

            elif abs(self.planet_aspects[j].JupiterDiff - 120) < 10:
               weights.JupiterWeight = 10 - (abs(self.planet_aspects[j].JupiterDiff - 120))
               weights.JupiterAspectType = 3
               weights.TotalAspect += weights.JupiterWeight
               weights.TotalTrine += weights.JupiterWeight
               weights.TotalGood += weights.JupiterWeight

            elif abs(self.planet_aspects[j].JupiterDiff - 180) < 10:
               weights.JupiterWeight = (10 - (abs(self.planet_aspects[j].JupiterDiff - 180))) * -1
               weights.JupiterAspectType = 4
               weights.TotalAspect += weights.JupiterWeight
               weights.TotalOpposite += weights.JupiterWeight
               weights.TotalBad += weights.JupiterWeight

            else:
               weights.JupiterWeight = 0
               weights.JupiterAspectType = 5

           # Aspect to Current Saturn
            if abs(self.planet_aspects[j].SaturnDiff - 0) < 10:
               weights.SaturnWeight = 10 - (abs(self.planet_aspects[j].SaturnDiff - 0))
               weights.SaturnAspectType = 0
               weights.TotalAspect += weights.SaturnWeight
               weights.TotalConjunct += weights.SaturnWeight
               weights.TotalGood += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff - 60) < 5:
               weights.SaturnWeight = 5 - (abs(self.planet_aspects[j].SaturnDiff - 60))
               weights.SaturnAspectType = 1
               weights.TotalAspect += weights.SaturnWeight
               weights.TotalSextile += weights.SaturnWeight
               weights.TotalGood += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff - 90) < 10:
               weights.SaturnWeight = (10 - (abs(self.planet_aspects[j].SaturnDiff - 90))) * -1
               weights.SaturnAspectType = 2
               weights.TotalAspect += weights.SaturnWeight
               weights.TotalSquare += weights.SaturnWeight
               weights.TotalBad += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff - 120) < 10:
               weights.SaturnWeight = 10 - (abs(self.planet_aspects[j].SaturnDiff - 120))
               weights.SaturnAspectType = 3
               weights.TotalAspect += weights.SaturnWeight
               weights.TotalTrine += weights.SaturnWeight
               weights.TotalGood += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff - 180) < 10:
               weights.SaturnWeight = (10 - (abs(self.planet_aspects[j].SaturnDiff - 180))) * -1
               weights.SaturnAspectType = 4
               weights.TotalAspect += weights.SaturnWeight
               weights.TotalOpposite += weights.SaturnWeight
               weights.TotalBad += weights.SaturnWeight
            else:
               weights.SaturnWeight = 0
               weights.SaturnAspectType = 5

            # Aspect to Current Uranus
            if abs(self.planet_aspects[j].UranusDiff - 0) < 10:
                weights.UranusWeight = 10 - (abs(self.planet_aspects[j].UranusDiff - 0))
                weights.UranusAspectType = 0
                weights.TotalAspect += weights.UranusWeight
                weights.TotalConjunct += weights.UranusWeight
                weights.TotalGood += weights.UranusWeight

            elif abs(self.planet_aspects[j].UranusDiff - 60) < 5:
                weights.UranusWeight = 5 - (abs(self.planet_aspects[j].UranusDiff - 60))
                weights.UranusAspectType = 1
                weights.TotalAspect += weights.UranusWeight
                weights.TotalSextile += weights.UranusWeight
                weights.TotalGood += weights.UranusWeight

            elif abs(self.planet_aspects[j].UranusDiff - 90) < 10:
                weights.UranusWeight = (10 - (abs(self.planet_aspects[j].UranusDiff - 90))) * -1
                weights.UranusAspectType = 2
                weights.TotalAspect += weights.UranusWeight
                weights.TotalSquare += weights.UranusWeight
                weights.TotalBad += weights.UranusWeight

            elif abs(self.planet_aspects[j].UranusDiff - 120) < 10:
                weights.UranusWeight = 10 - (abs(self.planet_aspects[j].UranusDiff - 120))
                weights.UranusAspectType = 3
                weights.TotalAspect += weights.UranusWeight
                weights.TotalTrine += weights.UranusWeight
                weights.TotalGood += weights.UranusWeight

            elif abs(self.planet_aspects[j].UranusDiff - 180) < 10:
                weights.UranusWeight = (10 - (abs(self.planet_aspects[j].UranusDiff - 180))) * -1
                weights.UranusAspectType = 4
                weights.TotalAspect += weights.UranusWeight
                weights.TotalOpposite += weights.UranusWeight
                weights.TotalBad += weights.UranusWeight
            else:
                weights.UranusWeight = 0
                weights.UranusAspectType = 5

            # Aspect to Current Neptune
            if abs(self.planet_aspects[j].NeptuneDiff - 0) < 10:
                weights.NeptuneWeight = 10 - (abs(self.planet_aspects[j].NeptuneDiff - 0))
                weights.NeptuneAspectType = 0
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalConjunct += weights.NeptuneWeight
                weights.TotalGood += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff - 60) < 5:
                weights.NeptuneWeight = 5 - (abs(self.planet_aspects[j].NeptuneDiff - 60))
                weights.NeptuneAspectType = 1
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalSextile += weights.NeptuneWeight
                weights.TotalGood += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff - 90) < 10:
                weights.NeptuneWeight = (10 - (abs(self.planet_aspects[j].NeptuneDiff - 90))) * -1
                weights.NeptuneAspectType = 2
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalSquare += weights.NeptuneWeight
                weights.TotalBad += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff - 120) < 10:
                weights.NeptuneWeight = 10 - (abs(self.planet_aspects[j].NeptuneDiff - 120))
                weights.NeptuneAspectType = 3
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalTrine += weights.NeptuneWeight
                weights.TotalGood += weights.NeptuneWeight

            elif abs(self.planet_aspects[j].NeptuneDiff - 180) < 10:
                weights.NeptuneWeight = (10 - (abs(self.planet_aspects[j].NeptuneDiff - 180))) * -1
                weights.NeptuneAspectType = 4
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalOpposite += weights.NeptuneWeight
                weights.TotalBad += weights.NeptuneWeight
            else:
                weights.NeptuneWeight = 0
                weights.NeptuneAspectType = 5

            # Aspect to Current Pluto
            if abs(self.planet_aspects[j].PlutoDiff - 0) < 10:
                weights.PlutoWeight = 10 - (abs(self.planet_aspects[j].PlutoDiff - 0))
                weights.PlutoAspectType = 0
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalConjunct += weights.PlutoWeight
                weights.TotalGood += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff - 60) < 5:
                weights.PlutoWeight = 5 - (abs(self.planet_aspects[j].PlutoDiff - 60))
                weights.PlutoAspectType = 1
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalSextile += weights.PlutoWeight
                weights.TotalGood += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff - 90) < 10:
                weights.PlutoWeight = (10 - (abs(self.planet_aspects[j].PlutoDiff - 90))) * -1
                weights.PlutoAspectType = 2
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalSquare += weights.PlutoWeight
                weights.TotalBad += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff - 120) < 10:
                weights.PlutoWeight = 10 - (abs(self.planet_aspects[j].PlutoDiff - 120))
                weights.PlutoAspectType = 3
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalTrine += weights.PlutoWeight
                weights.TotalGood += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff - 180) < 10:
                weights.PlutoWeight = (10 - (abs(self.planet_aspects[j].PlutoDiff - 180))) * -1
                weights.PlutoAspectType = 4
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalOpposite += weights.PlutoWeight
                weights.TotalBad += weights.PlutoWeight
            else:
                weights.PlutoWeight = 0
                weights.PlutoAspectType = 5

            # Aspect to Marker Right
            if abs(self.planet_aspects[j].MarkerDiff - 0) < 10:
                weights.MarkerWeight = 10 - (abs(self.planet_aspects[j].MarkerDiff - 0))
                weights.MarkerAspectType = 0
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerConjunct += weights.MarkerWeight
                weights.MarkerGood += weights.MarkerWeight
            elif abs(self.planet_aspects[j].MarkerDiff - 60) < 5:
                weights.MarkerWeight = 5 - (abs(self.planet_aspects[j].MarkerDiff - 60))
                weights.MarkerAspectType = 1
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerSextile += weights.MarkerWeight
                weights.MarkerGood += weights.MarkerWeight

            elif abs(self.planet_aspects[j].MarkerDiff - 90) < 10:
                weights.MarkerWeight = (10 - (abs(self.planet_aspects[j].MarkerDiff - 90))) * -1
                weights.MarkerAspectType = 2
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerSquare += weights.MarkerWeight
                weights.MarkerBad += weights.MarkerWeight
            elif abs(self.planet_aspects[j].MarkerDiff - 120) < 10:
                weights.MarkerWeight = 10 - (abs(self.planet_aspects[j].MarkerDiff - 120))
                weights.MarkerAspectType = 3
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerTrine += weights.MarkerWeight
                weights.MarkerGood += weights.MarkerWeight

            elif abs(self.planet_aspects[j].MarkerDiff - 180) < 10:
                weights.MarkerWeight = (10 - (abs(self.planet_aspects[j].MarkerDiff - 180))) * -1
                weights.MarkerAspectType = 4
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerOpposite += weights.MarkerWeight
                weights.MarkerBad += weights.MarkerWeight

            else:
                weights.MarkerWeight = 0
                weights.MarkerAspectType = 5

            self.natal_weight_list.append(weights)

            weights = PlanetWeightsStruct()

            # Aspect to Current Sun
            if abs(self.planet_aspects[j].SunDiff_Cur - 0) < 10:
                weights.SunWeight = 10 - (abs(self.planet_aspects[j].SunDiff_Cur - 0))
                weights.SunAspectType = 0
                weights.TotalAspect += weights.SunWeight
                weights.TotalConjunct += weights.SunWeight
                weights.TotalGood += weights.SunWeight
            elif abs(self.planet_aspects[j].SunDiff_Cur - 60) < 5:
                weights.SunWeight = 5 - (abs(self.planet_aspects[j].SunDiff_Cur - 60))
                weights.SunAspectType = 1
                weights.TotalAspect += weights.SunWeight
                weights.TotalSextile += weights.SunWeight
                weights.TotalGood += weights.SunWeight
            elif abs(self.planet_aspects[j].SunDiff_Cur - 90) < 10:
                weights.SunWeight = (10 - (abs(self.planet_aspects[j].SunDiff_Cur - 90))) * -1
                weights.SunAspectType = 2
                weights.TotalAspect += weights.SunWeight
                weights.TotalSquare += weights.SunWeight
                weights.TotalBad += weights.SunWeight
            elif abs(self.planet_aspects[j].SunDiff_Cur - 120) < 10:
                weights.SunWeight = 10 - (abs(self.planet_aspects[j].SunDiff_Cur - 120))
                weights.SunAspectType = 3
                weights.TotalAspect += weights.SunWeight
                weights.TotalTrine += weights.SunWeight
                weights.TotalGood += weights.SunWeight
            elif abs(self.planet_aspects[j].SunDiff_Cur - 180) < 10:
                weights.SunWeight = (10 - (abs(self.planet_aspects[j].SunDiff_Cur - 180))) * -1
                weights.SunAspectType = 4
                weights.TotalAspect += weights.SunWeight
                weights.TotalOpposite += weights.SunWeight
                weights.TotalBad += weights.SunWeight
            else:
                weights.SunWeight = 0
                weights.SunAspectType = 5

            # Aspect to Current Moon
            if (abs(self.planet_aspects[j].MoonDiff_Cur - 0) < 10):
                weights.MoonWeight = 10 - (abs(self.planet_aspects[j].MoonDiff_Cur - 0))
                weights.MoonAspectType = 0
                weights.TotalAspect += weights.MoonWeight
                weights.TotalConjunct += weights.MoonWeight
                weights.TotalGood += weights.MoonWeight
            elif (abs(self.planet_aspects[j].MoonDiff_Cur - 60) < 5):
                weights.MoonWeight = 5 - (abs(self.planet_aspects[j].MoonDiff_Cur - 60))
                weights.MoonAspectType = 1
                weights.TotalAspect += weights.MoonWeight
                weights.TotalSextile += weights.MoonWeight
                weights.TotalGood += weights.MoonWeight
            elif (abs(self.planet_aspects[j].MoonDiff_Cur - 90) < 10):
                weights.MoonWeight = (10 - (abs(self.planet_aspects[j].MoonDiff_Cur - 90))) * -1
                weights.MoonAspectType = 2
                weights.TotalAspect += weights.MoonWeight
                weights.TotalSquare += weights.MoonWeight
                weights.TotalBad += weights.MoonWeight
            elif (abs(self.planet_aspects[j].MoonDiff_Cur - 120) < 10):
                weights.MoonWeight = 10 - (abs(self.planet_aspects[j].MoonDiff_Cur - 120))
                weights.MoonAspectType = 3
                weights.TotalAspect += weights.MoonWeight
                weights.TotalTrine += weights.MoonWeight
                weights.TotalGood += weights.MoonWeight
            elif (abs(self.planet_aspects[j].MoonDiff_Cur - 180) < 10):
                weights.MoonWeight = (10 - (abs(self.planet_aspects[j].MoonDiff_Cur - 180))) * -1
                weights.MoonAspectType = 4
                weights.TotalAspect += weights.MoonWeight
                weights.TotalOpposite += weights.MoonWeight
                weights.TotalBad += weights.MoonWeight
            else:
                weights.MoonWeight = 0
                weights.MoonAspectType = 5

            # Aspect to Current Venus
            if (abs(self.planet_aspects[j].VenusDiff_Cur - 0) < 10):
                weights.VenusWeight = 10 - (abs(self.planet_aspects[j].VenusDiff_Cur - 0))
                weights.VenusAspectType = 0
                weights.TotalAspect += weights.VenusWeight
                weights.TotalConjunct += weights.VenusWeight
                weights.TotalGood += weights.VenusWeight
            elif (abs(self.planet_aspects[j].VenusDiff_Cur - 60) < 5):
                weights.VenusWeight = 5 - (abs(self.planet_aspects[j].VenusDiff_Cur - 60))
                weights.VenusAspectType = 1
                weights.TotalAspect += weights.VenusWeight
                weights.TotalSextile += weights.VenusWeight
                weights.TotalGood += weights.VenusWeight
            elif (abs(self.planet_aspects[j].VenusDiff_Cur - 90) < 10):
                weights.VenusWeight = (10 - (abs(self.planet_aspects[j].VenusDiff_Cur - 90))) * -1
                weights.VenusAspectType = 2
                weights.TotalAspect += weights.VenusWeight
                weights.TotalSquare += weights.VenusWeight
                weights.TotalBad += weights.VenusWeight
            elif (abs(self.planet_aspects[j].VenusDiff_Cur - 120) < 10):
                weights.VenusWeight = 10 - (abs(self.planet_aspects[j].VenusDiff_Cur - 120))
                weights.VenusAspectType = 3
                weights.TotalAspect += weights.VenusWeight
                weights.TotalTrine += weights.VenusWeight
                weights.TotalGood += weights.VenusWeight
            elif (abs(self.planet_aspects[j].VenusDiff_Cur - 180) < 10):
                weights.VenusWeight = (10 - (abs(self.planet_aspects[j].VenusDiff_Cur - 180))) * -1
                weights.VenusAspectType = 4
                weights.TotalAspect += weights.VenusWeight
                weights.TotalOpposite += weights.VenusWeight
                weights.TotalBad += weights.VenusWeight
            else:
                weights.VenusWeight = 0
                weights.VenusAspectType = 5

            # Aspect to Current Mercury
            if (abs(self.planet_aspects[j].MercuryDiff_Cur - 0) < 10):
                weights.MercuryWeight = 10 - (abs(self.planet_aspects[j].MercuryDiff_Cur - 0))
                weights.MercuryAspectType = 0
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalConjunct += weights.MercuryWeight
                weights.TotalGood += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff_Cur - 60) < 5:
                weights.MercuryWeight = 5 - (abs(self.planet_aspects[j].MercuryDiff_Cur - 60))
                weights.MercuryAspectType = 1
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalSextile += weights.MercuryWeight
                weights.TotalGood += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff_Cur - 90) < 10:
                weights.MercuryWeight = (10 - (abs(self.planet_aspects[j].MercuryDiff_Cur - 90))) * -1
                weights.MercuryAspectType = 2
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalSquare += weights.MercuryWeight
                weights.TotalBad += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff_Cur - 120) < 10:
                weights.MercuryWeight = 10 - (abs(self.planet_aspects[j].MercuryDiff_Cur - 120))
                weights.MercuryAspectType = 3
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalTrine += weights.MercuryWeight
                weights.TotalGood += weights.MercuryWeight
            elif abs(self.planet_aspects[j].MercuryDiff_Cur - 180) < 10:
                weights.MercuryWeight = (10 - (abs(self.planet_aspects[j].MercuryDiff_Cur - 180))) * -1
                weights.MercuryAspectType = 4
                weights.TotalAspect += weights.MercuryWeight
                weights.TotalOpposite += weights.MercuryWeight
                weights.TotalBad += weights.MercuryWeight
            else:
                weights.MercuryWeight = 0
                weights.MercuryAspectType = 5

            # Aspect to Current Mars
            if abs(self.planet_aspects[j].MarsDiff_Cur - 0) < 10:
                weights.MarsWeight = 10 - (abs(self.planet_aspects[j].MarsDiff_Cur - 0))
                weights.MarsAspectType = 0
                weights.TotalAspect += weights.MarsWeight
                weights.TotalConjunct += weights.MarsWeight
                weights.TotalGood += weights.MarsWeight

            elif abs(self.planet_aspects[j].MarsDiff_Cur - 60) < 5:
                weights.MarsWeight = 5 - (abs(self.planet_aspects[j].MarsDiff_Cur - 60))
                weights.MarsAspectType = 1
                weights.TotalAspect += weights.MarsWeight
                weights.TotalSextile += weights.MarsWeight
                weights.TotalGood += weights.MarsWeight
            elif abs(self.planet_aspects[j].MarsDiff_Cur - 90) < 10:
                weights.MarsWeight = (10 - (abs(self.planet_aspects[j].MarsDiff_Cur - 90))) * -1
                weights.MarsAspectType = 2
                weights.TotalAspect += weights.MarsWeight
                weights.TotalSquare += weights.MarsWeight
                weights.TotalBad += weights.MarsWeight
            elif abs(self.planet_aspects[j].MarsDiff_Cur - 120) < 10:
                weights.MarsWeight = 10 - (abs(self.planet_aspects[j].MarsDiff_Cur - 120))
                weights.MarsAspectType = 3
                weights.TotalAspect += weights.MarsWeight
                weights.TotalTrine += weights.MarsWeight
                weights.TotalGood += weights.MarsWeight

            elif abs(self.planet_aspects[j].MarsDiff_Cur - 180) < 10:
                weights.MarsWeight = (10 - (abs(self.planet_aspects[j].MarsDiff_Cur - 180))) * -1
                weights.MarsAspectType = 4
                weights.TotalAspect += weights.MarsWeight
                weights.TotalOpposite += weights.MarsWeight
                weights.TotalBad += weights.MarsWeight
            else:
                weights.MarsWeight = 0
                weights.MarsAspectType = 5

            # Aspect to Current Jupiter
            if abs(self.planet_aspects[j].JupiterDiff_Cur - 0) < 10:
                weights.JupiterWeight = 10 - (abs(self.planet_aspects[j].JupiterDiff_Cur - 0))
                weights.JupiterAspectType = 0
                weights.TotalAspect += weights.JupiterWeight
                weights.TotalConjunct += weights.JupiterWeight
                weights.TotalGood += weights.JupiterWeight
            elif abs(self.planet_aspects[j].JupiterDiff_Cur - 60) < 5:
                weights.JupiterWeight = 5 - (abs(self.planet_aspects[j].JupiterDiff_Cur - 60))
                weights.JupiterAspectType = 1
                weights.TotalAspect += weights.JupiterWeight
                weights.TotalSextile += weights.JupiterWeight
                weights.TotalGood += weights.JupiterWeight
            elif abs(self.planet_aspects[j].JupiterDiff_Cur - 90) < 10:
                weights.JupiterWeight = (10 - (abs(self.planet_aspects[j].JupiterDiff_Cur - 90))) * -1
                weights.JupiterAspectType = 2
                weights.TotalAspect += weights.JupiterWeight
                weights.TotalSquare += weights.JupiterWeight
                weights.TotalBad += weights.JupiterWeight
            elif abs(self.planet_aspects[j].JupiterDiff_Cur - 120) < 10:
                weights.JupiterWeight = 10 - (abs(self.planet_aspects[j].JupiterDiff_Cur - 120))
                weights.JupiterAspectType = 3
                weights.TotalAspect += weights.JupiterWeight
                weights.TotalTrine += weights.JupiterWeight
                weights.TotalGood += weights.JupiterWeight
            elif abs(self.planet_aspects[j].JupiterDiff_Cur - 180) < 10:
                weights.JupiterWeight = (10 - (abs(self.planet_aspects[j].JupiterDiff_Cur - 180))) * -1
                weights.JupiterAspectType = 4
                weights.TotalAspect += weights.JupiterWeight
                weights.TotalOpposite += weights.JupiterWeight
                weights.TotalBad += weights.JupiterWeight
            else:
                weights.JupiterWeight = 0
                weights.JupiterAspectType = 5

            # Aspect to Current Saturn
            if (abs(self.planet_aspects[j].SaturnDiff_Cur - 0) < 10):
                weights.SaturnWeight = 10 - (abs(self.planet_aspects[j].SaturnDiff_Cur - 0))
                weights.SaturnAspectType = 0
                weights.TotalAspect += weights.SaturnWeight
                weights.TotalConjunct += weights.SaturnWeight
                weights.TotalGood += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff_Cur - 60) < 5:
                weights.SaturnWeight = 5 - (abs(self.planet_aspects[j].SaturnDiff_Cur - 60))
                weights.SaturnAspectType = 1
                weights.TotalAspect += weights.SaturnWeight
                weights.TotalSextile += weights.SaturnWeight
                weights.TotalGood += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff_Cur - 90) < 10:
                weights.SaturnWeight = (10 - (abs(self.planet_aspects[j].SaturnDiff_Cur - 90))) * -1
                weights.SaturnAspectType = 2
                weights.TotalAspect += weights.SaturnWeight
                weights.TotalSquare += weights.SaturnWeight
                weights.TotalBad += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff_Cur - 120) < 10:
                weights.SaturnWeight = 10 - (abs(self.planet_aspects[j].SaturnDiff_Cur - 120))
                weights.SaturnAspectType = 3
                weights.TotalAspect += weights.SaturnWeight
                weights.TotalTrine += weights.SaturnWeight
                weights.TotalGood += weights.SaturnWeight
            elif abs(self.planet_aspects[j].SaturnDiff_Cur - 180) < 10:
                weights.SaturnWeight = (10 - (abs(self.planet_aspects[j].SaturnDiff_Cur - 180))) * -1
                weights.SaturnAspectType = 4
                weights.TotalAspect += weights.SaturnWeight
                weights.TotalOpposite += weights.SaturnWeight
                weights.TotalBad += weights.SaturnWeight
            else:
                weights.SaturnWeight = 0
                weights.SaturnAspectType = 5


            # Aspect to Current Uranus
            if abs(self.planet_aspects[j].UranusDiff_Cur - 0) < 10:
                weights.UranusWeight = 10 - (abs(self.planet_aspects[j].UranusDiff_Cur - 0))
                weights.UranusAspectType = 0
                weights.TotalAspect += weights.UranusWeight
                weights.TotalConjunct += weights.UranusWeight
                weights.TotalGood += weights.UranusWeight
            elif abs(self.planet_aspects[j].UranusDiff_Cur - 60) < 5:
                weights.UranusWeight = 5 - (abs(self.planet_aspects[j].UranusDiff_Cur - 60))
                weights.UranusAspectType = 1
                weights.TotalAspect += weights.UranusWeight
                weights.TotalSextile += weights.UranusWeight
                weights.TotalGood += weights.UranusWeight
            elif abs(self.planet_aspects[j].UranusDiff_Cur - 90) < 10:
                weights.UranusWeight = (10 - (abs(self.planet_aspects[j].UranusDiff_Cur - 90))) * -1
                weights.UranusAspectType = 2
                weights.TotalAspect += weights.UranusWeight
                weights.TotalSquare += weights.UranusWeight
                weights.TotalBad += weights.UranusWeight
            elif abs(self.planet_aspects[j].UranusDiff_Cur - 120) < 10:
                weights.UranusWeight = 10 - (abs(self.planet_aspects[j].UranusDiff_Cur - 120))
                weights.UranusAspectType = 3
                weights.TotalAspect += weights.UranusWeight
                weights.TotalTrine += weights.UranusWeight
                weights.TotalGood += weights.UranusWeight
            elif abs(self.planet_aspects[j].UranusDiff_Cur - 180) < 10:
                weights.UranusWeight = (10 - (abs(self.planet_aspects[j].UranusDiff_Cur - 180))) * -1
                weights.UranusAspectType = 4
                weights.TotalAspect += weights.UranusWeight
                weights.TotalOpposite += weights.UranusWeight
                weights.TotalBad += weights.UranusWeight
            else:
                weights.UranusWeight = 0
                weights.UranusAspectType = 5

            # Aspect to Current Neptune
            if abs(self.planet_aspects[j].NeptuneDiff_Cur - 0) < 10:
                weights.NeptuneWeight = 10 - (abs(self.planet_aspects[j].NeptuneDiff_Cur - 0))
                weights.NeptuneAspectType = 0
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalConjunct += weights.NeptuneWeight
                weights.TotalGood += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff_Cur - 60) < 5:
                weights.NeptuneWeight = 5 - (abs(self.planet_aspects[j].NeptuneDiff_Cur - 60))
                weights.NeptuneAspectType = 1
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalSextile += weights.NeptuneWeight
                weights.TotalGood += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff_Cur - 90) < 10:
                weights.NeptuneWeight = (10 - (abs(self.planet_aspects[j].NeptuneDiff_Cur - 90))) * -1
                weights.NeptuneAspectType = 2
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalSquare += weights.NeptuneWeight
                weights.TotalBad += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff_Cur - 120) < 10:
                weights.NeptuneWeight = 10 - (abs(self.planet_aspects[j].NeptuneDiff_Cur - 120))
                weights.NeptuneAspectType = 3
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalTrine += weights.NeptuneWeight
                weights.TotalGood += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff_Cur - 180) < 10:
                weights.NeptuneWeight = (10 - (abs(self.planet_aspects[j].NeptuneDiff_Cur - 180))) * -1
                weights.NeptuneAspectType = 4
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalOpposite += weights.NeptuneWeight
                weights.TotalBad += weights.NeptuneWeight
            elif abs(self.planet_aspects[j].NeptuneDiff_Cur - 180) < 10:
                weights.NeptuneWeight = (10 - (abs(self.planet_aspects[j].NeptuneDiff_Cur - 180))) * -1
                weights.NeptuneAspectType = 4
                weights.TotalAspect += weights.NeptuneWeight
                weights.TotalOpposite += weights.NeptuneWeight
                weights.TotalBad += weights.NeptuneWeight
            else:
                weights.NeptuneWeight = 0
                weights.NeptuneAspectType = 5

            # Aspect to Current Pluto
            if abs(self.planet_aspects[j].PlutoDiff_Cur - 0) < 10:
                weights.PlutoWeight = 10 - (abs(self.planet_aspects[j].PlutoDiff_Cur - 0))
                weights.PlutoAspectType = 0
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalConjunct += weights.PlutoWeight
                weights.TotalGood += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff_Cur - 60) < 5:
                weights.PlutoWeight = 5 - (abs(self.planet_aspects[j].PlutoDiff_Cur - 60))
                weights.PlutoAspectType = 1
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalSextile += weights.PlutoWeight
                weights.TotalGood += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff_Cur - 90) < 10:
                weights.PlutoWeight = (10 - (abs(self.planet_aspects[j].PlutoDiff_Cur - 90))) * -1
                weights.PlutoAspectType = 2
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalSquare += weights.PlutoWeight
                weights.TotalBad += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff_Cur - 120) < 10:
                weights.PlutoWeight = 10 - (abs(self.planet_aspects[j].PlutoDiff_Cur - 120))
                weights.PlutoAspectType = 3
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalTrine += weights.PlutoWeight
                weights.TotalGood += weights.PlutoWeight
            elif abs(self.planet_aspects[j].PlutoDiff_Cur - 180) < 10:
                weights.PlutoWeight = (10 - (abs(self.planet_aspects[j].PlutoDiff_Cur - 180))) * -1
                weights.PlutoAspectType = 4
                weights.TotalAspect += weights.PlutoWeight
                weights.TotalOpposite += weights.PlutoWeight
                weights.TotalBad += weights.PlutoWeight
            else:
                weights.PlutoWeight = 0
                weights.PlutoAspectType = 5

            # Aspect to Marker Left
            if abs(self.planet_aspects[j].MarkerDiff_Cur - 0) < 10:
                weights.MarkerWeight = 10 - (abs(self.planet_aspects[j].MarkerDiff_Cur - 0))
                weights.MarkerAspectType = 0
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerConjunct += weights.MarkerWeight
                weights.MarkerGood += weights.MarkerWeight
            elif abs(self.planet_aspects[j].MarkerDiff_Cur - 60) < 5:
                weights.MarkerWeight = 5 - (abs(self.planet_aspects[j].MarkerDiff_Cur - 60))
                weights.MarkerAspectType = 1
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerSextile += weights.MarkerWeight
                weights.MarkerGood += weights.MarkerWeight
            elif abs(self.planet_aspects[j].MarkerDiff_Cur - 90) < 10:
                weights.MarkerWeight = (10 - (abs(self.planet_aspects[j].MarkerDiff_Cur - 90))) * -1
                weights.MarkerAspectType = 2
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerSquare += weights.MarkerWeight
                weights.MarkerBad += weights.MarkerWeight
            elif abs(self.planet_aspects[j].MarkerDiff_Cur - 120) < 10:
                weights.MarkerWeight = 10 - (abs(self.planet_aspects[j].MarkerDiff_Cur - 120))
                weights.MarkerAspectType = 3
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerTrine += weights.MarkerWeight
                weights.MarkerGood += weights.MarkerWeight
            elif abs(self.planet_aspects[j].MarkerDiff_Cur - 180) < 10:
                weights.MarkerWeight = (10 - (abs(self.planet_aspects[j].MarkerDiff_Cur - 180))) * -1
                weights.MarkerAspectType = 4
                weights.MarkerAspect += weights.MarkerWeight
                weights.MarkerOpposite += weights.MarkerWeight
                weights.MarkerBad += weights.MarkerWeight
            else:
                weights.MarkerWeight = 0
                weights.MarkerAspectType = 5

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
            print("chakra_list house loop = ", house)

            # Aggregate weight data for this house
            for j in range(10):
                print("weight j loop = ", j)
                if self.current_planets_2[j].house == house:
                    chakra.current_good += self.current_weight_list[j].total_good
                    chakra.current_bad += self.current_weight_list[j].total_bad
                    chakra.current_total += self.current_weight_list[j].total_aspect

                if self.natal_planets[j].house == house:
                    chakra.natal_good += self.natal_weight_list[j].total_good
                    chakra.natal_bad += self.natal_weight_list[j].total_bad
                    chakra.natal_total += self.natal_weight_list[j].total_aspect

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
