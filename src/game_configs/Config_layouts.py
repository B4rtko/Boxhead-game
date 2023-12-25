from dataclasses import dataclass

from typing import Tuple


@dataclass
class ConfigControlScreenLayout:
    """Class for storing game's main menu control elements layout"""
    góra: Tuple[int, int] = (1303, 79)
    dół: Tuple[int, int] = (1303, 208)
    lewo: Tuple[int, int] = (1303, 338)
    prawo: Tuple[int, int] = (1303, 468)
    strzał: Tuple[int, int] = (1303, 598)
    następna: Tuple[int, int] = (1303, 728)
    poprzednia: Tuple[int, int] = (1303, 858)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class ConfigDifficultyScreenLayout:
    """Class for storing game's main menu difficulty elements layout"""
    łatwy: Tuple[int, int] = (1303, 338)
    średni: Tuple[int, int] = (1303, 468)
    trudny: Tuple[int, int] = (1303, 598)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class ConfigOptionScreenLayout:
    """Class for storing game's main menu option elements layout"""
    mapa: Tuple[int, int] = (520, 275)
    sterowanie: Tuple[int, int] = (520, 405)
    trudność: Tuple[int, int] = (520, 535)
    powrót: Tuple[int, int] = (520, 665)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class ConfigPauseScreenLayout:
    """Class for storing game's main menu pause elements layout"""
    wznów: Tuple[int, int] = (1130, 519)
    zakończ: Tuple[int, int] = (1130, 650)

    def __getitem__(self, item):
        return getattr(self, item)



@dataclass
class ConfigStartScreenLayout:
    """Class for storing game's main menu start screen elements layout"""
    graj: Tuple[int, int] = (520, 140)
    opcje: Tuple[int, int] = (520, 275)
    instrukcja: Tuple[int, int] = (520, 405)
    wyniki: Tuple[int, int] = (520, 535)
    o_autorze: Tuple[int, int] = (520, 665)
    zakoncz: Tuple[int, int] = (520, 795)

    def __getitem__(self, item):
        if item == "o autorze":
            item = "o_autorze"

        return getattr(self, item)


config_control_screen_layout = ConfigControlScreenLayout()
config_difficulty_screen_layout = ConfigDifficultyScreenLayout()
config_option_screen_layout = ConfigOptionScreenLayout()
config_pause_screen_layout = ConfigPauseScreenLayout()
config_start_screen_layout = ConfigStartScreenLayout()
