from pygame.math import Vector2


class SectorBotDirectionsBase:
    @property
    def dir_match_direction(self):
        raise NotImplementedError

    @property
    def dir_vector(self):
        raise NotImplementedError

    @property
    def dir_match_close_sectors(self):
        raise NotImplementedError


class Sector1BotDirections(SectorBotDirectionsBase):
    dir_match_direction = {}
    dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                  "right": Vector2(1,0), "down": Vector2(0,1)}

    _close_to_11 = [11]
    dir_match_close_sectors = {11: _close_to_11}


class Sector2BotDirections(SectorBotDirectionsBase):
    _dir_dict11 = {12: "right", 13: "right", 14: "right", 15: "right",
                   22: "right", 25: "right",
                   32: "right", 35: "right",
                   41: "right", 42: "right", 43: "right", 44: "right", 45: "right"}
    _dir_dict12 = {11: "left", 13: "right", 14: "right", 15: "right",
                   22: "down", 25: "right",
                   32: "down", 35: "right",
                   41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}
    _dir_dict13 = {11: "left", 12: "left", 14: "right", 15: "right",
                   22: "left", 25: "right",
                   32: "left", 35: "right",
                   41: "left", 42: "left", 43: "left", 44: "right", 45: "right"}
    _dir_dict14 = {11: "left", 12: "left", 13: "left", 15: "right",
                   22: "left", 25: "right",
                   32: "left", 35: "right",
                   41: "left", 42: "left", 43: "left", 44: "right", 45: "right"}
    _dir_dict15 = {11: "left", 12: "left", 13: "left", 14: "left",
                   22: "left", 25: "down",
                   32: "left", 35: "down",
                   41: "left", 42: "left", 43: "down", 44: "down", 45: "down"}

    _dir_dict22 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                   25: "up",
                   32: "down", 35: "down",
                   41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}
    _dir_dict25 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                   22: "up",
                   32: "up", 35: "down",
                   41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}

    _dir_dict32 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                   22: "up", 25: "up",
                   35: "down",
                   41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}
    _dir_dict35 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                   22: "down", 25: "up",
                   32: "down",
                   41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}

    _dir_dict41 = {11: "right", 12: "right", 13: "right", 14: "right", 15: "right",
                   22: "right", 25: "right",
                   32: "right", 35: "right",
                   42: "right", 43: "right", 44: "right", 45: "right"}
    _dir_dict42 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                   22: "up", 25: "right",
                   32: "up", 35: "right",
                   41: "left", 43: "right", 44: "right", 45: "right"}
    _dir_dict43 = {11: "left", 12: "left", 13: "left", 14: "left", 15: "right",
                   22: "left", 25: "right",
                   32: "left", 35: "right",
                   41: "left", 42: "left", 44: "right", 45: "right"}
    _dir_dict44 = {11: "left", 12: "left", 13: "left", 14: "right", 15: "right",
                   22: "left", 25: "right",
                   32: "left", 35: "right",
                   41: "left", 42: "left", 43: "left", 45: "right"}
    _dir_dict45 = {11: "left", 12: "left", 13: "up", 14: "up", 15: "up",
                   22: "left", 25: "up",
                   32: "left", 35: "up",
                   41: "left", 42: "left", 43: "left", 44: "left"}


    dir_match_direction = {11: _dir_dict11, 12: _dir_dict12, 13: _dir_dict13, 14: _dir_dict14, 15: _dir_dict15,
                           22: _dir_dict22, 25: _dir_dict25, 32: _dir_dict32, 35: _dir_dict35,
                           41: _dir_dict41, 42: _dir_dict42, 43: _dir_dict43, 44: _dir_dict44, 45: _dir_dict45}
    
    dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                  "right": Vector2(1,0), "down": Vector2(0,1)}

    _close_to_11 = [11, 12]
    _close_to_12 = [12, 11, 13, 22]
    _close_to_13 = [13, 12, 14]
    _close_to_14 = [14, 13, 15]
    _close_to_15 = [15, 14, 25]

    _close_to_22 = [22, 12, 32]
    _close_to_25 = [25, 15, 35]

    _close_to_32 = [32, 22, 42]
    _close_to_35 = [35, 25, 45]

    _close_to_41 = [41, 42]
    _close_to_42 = [42, 41, 43, 32]
    _close_to_43 = [43, 42, 44]
    _close_to_44 = [44, 43, 45]
    _close_to_45 = [45, 44, 35]

    dir_match_close_sectors = {11: _close_to_11, 12: _close_to_12, 13: _close_to_13, 14: _close_to_14, 15: _close_to_15,
                    22: _close_to_22, 25: _close_to_25,
                    32: _close_to_32, 35: _close_to_35,
                    41: _close_to_41, 42: _close_to_42, 43: _close_to_43, 44: _close_to_44, 45: _close_to_45}


class Sector3BotDirections(SectorBotDirectionsBase):
    _dir_dict11 = {12: "right", 13: "right", 14: "right", 15: "right", 16: "right",
                    21: "down", 26: "right",
                    31: "down", 33: "down", 34: "down", 36: "right",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
    _dir_dict12 = {11: "left", 13: "right", 14: "right", 15: "right", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "left", 34: "left", 36: "right",
                    41: "left", 42: "left", 43: "left", 44: "left", 45: "right", 46: "right"}
    _dir_dict13 = {11: "left", 12: "left", 14: "right", 15: "right", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "left", 34: "right", 36: "right",
                    41: "left", 42: "left", 43: "left", 44: "right", 45: "right", 46: "right"}
    _dir_dict14 = {11: "left", 12: "left", 13: "left", 15: "right", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "right", 34: "right", 36: "right",
                    41: "left", 42: "left", 43: "right", 44: "right", 45: "right", 46: "right"}
    _dir_dict15 = {11: "left", 12: "left", 13: "left", 14: "left", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "right", 34: "right", 36: "right",
                    41: "left", 42: "right", 43: "right", 44: "right", 45: "right", 46: "right"}
    _dir_dict16 = {11: "left", 12: "left", 13: "left", 14: "left", 15: "left",
                    21: "left", 26: "down",
                    31: "left", 33: "down", 34: "down", 36: "down",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}

    _dir_dict21 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                    26: "up",
                    31: "down", 33: "down", 34: "down", 36: "up",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
    _dir_dict26 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                    21: "up",
                    31: "down", 33: "down", 34: "down", 36: "down",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}

    _dir_dict31 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                    21: "up", 26: "down",
                    33: "down", 34: "down", 36: "down",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
    _dir_dict33 = {11: "down", 12: "down", 13: "down", 14: "down", 15: "down", 16: "down",
                    21: "down", 26: "down",
                    31: "down", 34: "right", 36: "down",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
    _dir_dict34 = {11: "down", 12: "down", 13: "down", 14: "down", 15: "down", 16: "down",
                    21: "down", 26: "down",
                    31: "down", 33: "left", 36: "down",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
    _dir_dict36 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                    21: "down", 26: "up",
                    31: "down", 33: "down", 34: "down",
                    41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}

    _dir_dict41 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "right",
                    21: "up", 26: "right",
                    31: "up", 33: "right", 34: "right", 36: "right",
                    42: "right", 43: "right", 44: "right", 45: "right", 46: "right"}
    _dir_dict42 = {11: "left", 12: "left", 13: "left", 14: "left", 15: "right", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "right", 34: "right", 36: "right",
                    41: "left", 43: "right", 44: "right", 45: "right", 46: "right"}
    _dir_dict43 = {11: "left", 12: "left", 13: "left", 14: "right", 15: "right", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "up", 34: "up", 36: "right",
                    41: "left", 42: "left", 44: "right", 45: "right", 46: "right"}
    _dir_dict44 = {11: "left", 12: "left", 13: "right", 14: "right", 15: "right", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "up", 34: "up", 36: "right",
                    41: "left", 42: "left", 43: "left", 45: "right", 46: "right"}
    _dir_dict45 = {11: "left", 12: "right", 13: "right", 14: "right", 15: "right", 16: "right",
                    21: "left", 26: "right",
                    31: "left", 33: "left", 34: "left", 36: "right",
                    41: "left", 42: "left", 43: "left", 44: "left", 46: "right"}
    _dir_dict46 = {11: "left", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                    21: "left", 26: "up",
                    31: "left", 33: "left", 34: "left", 36: "up",
                    41: "left", 42: "left", 43: "left", 44: "left", 45: "left"}


    dir_match_direction = {11: _dir_dict11, 12: _dir_dict12, 13: _dir_dict13, 14: _dir_dict14, 15: _dir_dict15, 16: _dir_dict16,
                           21: _dir_dict21, 26: _dir_dict26,
                           31: _dir_dict31, 33: _dir_dict33, 34: _dir_dict34, 36: _dir_dict36,
                           41: _dir_dict41, 42: _dir_dict42, 43: _dir_dict43, 44: _dir_dict44, 45: _dir_dict45, 46: _dir_dict46}

    dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                    "right": Vector2(1,0), "down": Vector2(0,1)}

    _close_to_11 = [11, 12, 21]
    _close_to_12 = [12, 11, 13]
    _close_to_13 = [13, 12, 14]
    _close_to_14 = [14, 13, 15]
    _close_to_15 = [15, 14, 16]
    _close_to_16 = [16, 15, 26]

    _close_to_21 = [21, 11, 31]
    _close_to_26 = [26, 16, 36]

    _close_to_31 = [31, 21, 41]
    _close_to_33 = [33, 34, 43, 44]
    _close_to_34 = [34, 33, 44, 43]
    _close_to_36 = [36, 26, 46]

    _close_to_41 = [41, 31, 42]
    _close_to_42 = [42, 41, 43]
    _close_to_43 = [43, 42, 44, 33, 34]
    _close_to_44 = [44, 43, 45, 34, 33]
    _close_to_45 = [45, 44, 46]
    _close_to_46 = [46, 45, 36]

    dir_match_close_sectors = {11: _close_to_11, 12: _close_to_12, 13: _close_to_13, 14: _close_to_14, 15: _close_to_15, 16: _close_to_16,
                               21: _close_to_21, 26: _close_to_26,
                               31: _close_to_31, 33: _close_to_33, 34: _close_to_34, 36: _close_to_36,
                               41: _close_to_41, 42: _close_to_42, 43: _close_to_43, 44: _close_to_44, 45: _close_to_45, 46: _close_to_46}


class Sector4BotDirections(SectorBotDirectionsBase):
    _dir_dict11 = {12: "right", 13: "right",
                   23: "right",
                   31: "right", 32: "right", 33: "right",
                   41: "right",
                   51: "right", 52: "right", 53: "right"}
    _dir_dict12 = {11: "left", 13: "right",
                   23: "right",
                   31: "right", 32: "right", 33: "right",
                   41: "right",
                   51: "right", 52: "right", 53: "right"}
    _dir_dict13 = {11: "left", 12: "left",
                   23: "down",
                   31: "down", 32: "down", 33: "down",
                   41: "down",
                   51: "down", 52: "down", 53: "down"}

    _dir_dict23 = {11: "up", 12: "up", 13: "up",
                   31: "down", 32: "down", 33: "down",
                   41: "down",
                   51: "down", 52: "down", 53: "down"}

    _dir_dict31 = {11: "right", 12: "right", 13: "right",
                   23: "right",
                   32: "right", 33: "right",
                   41: "down",
                   51: "down", 52: "down", 53: "down"}
    _dir_dict32 = {11: "right", 12: "right", 13: "right",
                   23: "right",
                   31: "left", 33: "right",
                   41: "left",
                   51: "left", 52: "left", 53: "left"}
    _dir_dict33 = {11: "up", 12: "up", 13: "up",
                   23: "up",
                   31: "left", 32: "left",
                   41: "left",
                   51: "left", 52: "left", 53: "left"}

    _dir_dict41 = {11: "up", 12: "up", 13: "up",
                   23: "up",
                   31: "up", 32: "up", 33: "up",
                   51: "down", 52: "down", 53: "down"}

    _dir_dict51 = {11: "up", 12: "up", 13: "up",
                   23: "up",
                   31: "up", 32: "up", 33: "up",
                   41: "up",
                   52: "right", 53: "right"}
    _dir_dict52 = {11: "left", 12: "left", 13: "left",
                   23: "left",
                   31: "left", 32: "left", 33: "left",
                   41: "left",
                   51: "left", 53: "right"}
    _dir_dict53 = {11: "left", 12: "left", 13: "left",
                   23: "left",
                   31: "left", 32: "left", 33: "left",
                   41: "left",
                   51: "left", 52: "left"}


    dir_match_direction = {11: _dir_dict11, 12: _dir_dict12, 13: _dir_dict13,
                           23: _dir_dict23,
                           31: _dir_dict31, 32: _dir_dict32, 33: _dir_dict33,
                           41: _dir_dict41,
                           51: _dir_dict51, 52: _dir_dict52, 53: _dir_dict53}

    dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                    "right": Vector2(1,0), "down": Vector2(0,1)}

    _close_to_11 = [11, 12]
    _close_to_12 = [12, 11, 13]
    _close_to_13 = [13, 12, 23]

    _close_to_23 = [23, 13, 33]

    _close_to_31 = [31, 32, 41]
    _close_to_32 = [32, 31, 33]
    _close_to_33 = [33, 32, 23]

    _close_to_41 = [41, 31, 51]

    _close_to_51 = [51, 41, 52]
    _close_to_52 = [52, 51, 53]
    _close_to_53 = [53, 52]

    dir_match_close_sectors = {11: _close_to_11, 12: _close_to_12, 13: _close_to_13,
                               23: _close_to_23,
                               31: _close_to_31, 32: _close_to_32, 33: _close_to_33,
                               41: _close_to_41,
                               51: _close_to_51, 52: _close_to_52, 53: _close_to_53}


class Sector5BotDirections(SectorBotDirectionsBase):
    _dir_dict11 = {12: "right", 15: "downright", 16: "downright",
                  21: "down", 22: "downright", 25: "downright", 26: "downright",
                  31: "down", 32: "downright", 33: "downright", 34: "downright", 35: "downright", 36: "downright",
                  43: "downright", 44: "downright",
                  53: "downright", 54: "downright",
                  61: "downright", 62: "downright", 63: "downright", 64: "downright", 65: "downright", 66: "downright",
                  71: "downright", 72: "downright", 75: "downright", 76: "downright",
                  81: "downright", 82: "downright", 85: "downright", 86: "downright"}
    _dir_dict12 = {11: "left", 15: "down", 16: "down",
                  21: "downleft", 22: "down", 25: "down", 26: "down",
                  31: "downleft", 32: "down", 33: "down", 34: "down", 35: "down", 36: "down",
                  43: "down", 44: "down",
                  53: "down", 54: "down",
                  61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                  71: "down", 72: "down", 75: "down", 76: "down",
                  81: "down", 82: "down", 85: "down", 86: "down"}
    _dir_dict15 = {11: "down", 12: "down", 16: "right",
                  21: "down", 22: "down", 25: "down", 26: "downright",
                  31: "down", 32: "down", 33: "down", 34: "down", 35: "down", 36: "downright",
                  43: "down", 44: "down",
                  53: "down", 54: "down",
                  61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                  71: "down", 72: "down", 75: "down", 76: "down",
                  81: "down", 82: "down", 85: "down", 86: "down"}
    _dir_dict16 = {11: "downleft", 12: "downleft", 15: "left",
                  21: "downleft", 22: "downleft", 25: "downleft", 26: "down",
                  31: "downleft", 32: "downleft", 33: "downleft", 34: "downleft", 35: "downleft", 36: "down",
                  43: "downleft", 44: "downleft",
                  53: "downleft", 54: "downleft",
                  61: "downleft", 62: "downleft", 63: "downleft", 64: "downleft", 65: "downleft", 66: "downleft",
                  71: "downleft", 72: "downleft", 75: "downleft", 76: "downleft",
                  81: "downleft", 82: "downleft", 85: "downleft", 86: "downleft"}

    _dir_dict21 = {11: "up", 12: "upright", 15: "downright", 16: "downright",
                  22: "right", 25: "downright", 26: "downright",
                  31: "down", 32: "downright", 33: "downright", 34: "downright", 35: "downright", 36: "downright",
                  43: "downright", 44: "downright",
                  53: "downright", 54: "downright",
                  61: "downright", 62: "downright", 63: "downright", 64: "downright", 65: "downright", 66: "downright",
                  71: "downright", 72: "downright", 75: "downright", 76: "downright",
                  81: "downright", 82: "downright", 85: "downright", 86: "downright"}
    _dir_dict22 = {11: "upleft", 12: "up", 15: "down", 16: "down",
                  21: "left", 25: "down", 26: "down",
                  31: "downleft", 32: "down", 33: "down", 34: "down", 35: "down", 36: "down",
                  43: "down", 44: "down",
                  53: "down", 54: "down",
                  61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                  71: "down", 72: "down", 75: "down", 76: "down",
                  81: "down", 82: "down", 85: "down", 86: "down"}
    _dir_dict25 = {11: "down", 12: "down", 15: "up", 16: "upright",
                  21: "down", 22: "down", 26: "right",
                  31: "down", 32: "down", 33: "down", 34: "down", 35: "down", 36: "downright",
                  43: "down", 44: "down",
                  53: "down", 54: "down",
                  61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                  71: "down", 72: "down", 75: "down", 76: "down",
                  81: "down", 82: "down", 85: "down", 86: "down"}
    _dir_dict26 = {11: "downleft", 12: "downleft", 15: "upleft", 16: "up",
                  21: "downleft", 22: "downleft", 25: "left",
                  31: "downleft", 32: "downleft", 33: "downleft", 34: "downleft", 35: "downleft", 36: "down",
                  43: "downleft", 44: "downleft",
                  53: "downleft", 54: "downleft",
                  61: "downleft", 62: "downleft", 63: "downleft", 64: "downleft", 65: "downleft", 66: "downleft",
                  71: "downleft", 72: "downleft", 75: "downleft", 76: "downleft",
                  81: "downleft", 82: "downleft", 85: "downleft", 86: "downleft"}

    _dir_dict31 = {11: "up", 12: "upright", 15: "right", 16: "right",
                  21: "up", 22: "upright", 25: "right", 26: "right",
                  32: "right", 33: "right", 34: "right", 35: "right", 36: "right",
                  43: "right", 44: "right",
                  53: "right", 54: "right",
                  61: "right", 62: "right", 63: "right", 64: "right", 65: "right", 66: "right",
                  71: "right", 72: "right", 75: "right", 76: "right",
                  81: "right", 82: "right", 85: "right", 86: "right"}
    _dir_dict32 = {11: "upleft", 12: "up", 15: "right", 16: "right",
                  21: "upleft", 22: "up", 25: "right", 26: "right",
                  31: "left", 33: "right", 34: "right", 35: "right", 36: "right",
                  43: "right", 44: "right",
                  53: "right", 54: "right",
                  61: "right", 62: "right", 63: "right", 64: "right", 65: "right", 66: "right",
                  71: "right", 72: "right", 75: "right", 76: "right",
                  81: "right", 82: "right", 85: "right", 86: "right"}
    _dir_dict33 = {11: "left", 12: "left", 15: "right", 16: "right",
                  21: "left", 22: "left", 25: "right", 26: "right",
                  31: "left", 32: "left", 34: "right", 35: "right", 36: "right",
                  43: "down", 44: "downright",
                  53: "down", 54: "downright",
                  61: "down", 62: "down", 63: "down", 64: "downright", 65: "downright", 66: "downright",
                  71: "down", 72: "down", 75: "downright", 76: "downright",
                  81: "down", 82: "down", 85: "downright", 86: "downright"}
    _dir_dict34 = {11: "left", 12: "left", 15: "right", 16: "right",
                  21: "left", 22: "left", 25: "right", 26: "right",
                  31: "left", 32: "left", 33: "left", 35: "right", 36: "right",
                  43: "downleft", 44: "down",
                  53: "downleft", 54: "down",
                  61: "downleft", 62: "downleft", 63: "downleft", 64: "down", 65: "down", 66: "down",
                  71: "downleft", 72: "downleft", 75: "down", 76: "down",
                  81: "downleft", 82: "downleft", 85: "down", 86: "down"}
    _dir_dict35 = {11: "left", 12: "left", 15: "up", 16: "upright",
                  21: "left", 22: "left", 25: "up", 26: "upright",
                  31: "left", 32: "left", 33: "left", 34: "left", 36: "right",
                  43: "left", 44: "left",
                  53: "left", 54: "left",
                  61: "left", 62: "left", 63: "left", 64: "left", 65: "left", 66: "left",
                  71: "left", 72: "left", 75: "left", 76: "left",
                  81: "left", 82: "left", 85: "left", 86: "left"}
    _dir_dict36 = {11: "left", 12: "left", 15: "upleft", 16: "up",
                  21: "left", 22: "left", 25: "upleft", 26: "up",
                  31: "left", 32: "left", 33: "left", 34: "left", 35: "left",
                  43: "left", 44: "left",
                  53: "left", 54: "left",
                  61: "left", 62: "left", 63: "left", 64: "left", 65: "left", 66: "left",
                  71: "left", 72: "left", 75: "left", 76: "left",
                  81: "left", 82: "left", 85: "left", 86: "left"}

    _dir_dict43 = {11: "up", 12: "up", 15: "upright", 16: "upright",
                  21: "up", 22: "up", 25: "upright", 26: "upright",
                  31: "up", 32: "up", 33: "up", 34: "upright", 35: "upright", 36: "upright",
                  44: "right",
                  53: "down", 54: "downright",
                  61: "down", 62: "down", 63: "down", 64: "downright", 65: "downright", 66: "downright",
                  71: "down", 72: "down", 75: "downright", 76: "downright",
                  81: "down", 82: "down", 85: "downright", 86: "downright"}
    _dir_dict44 = {11: "upleft", 12: "upleft", 15: "up", 16: "up",
                  21: "upleft", 22: "upleft", 25: "up", 26: "up",
                  31: "upleft", 32: "upleft", 33: "upleft", 34: "up", 35: "up", 36: "up",
                  43: "left",
                  53: "downleft", 54: "down",
                  61: "downleft", 62: "downleft", 63: "downleft", 64: "down", 65: "down", 66: "down",
                  71: "downleft", 72: "downleft", 75: "down", 76: "down",
                  81: "downleft", 82: "downleft", 85: "down", 86: "down"}

    _dir_dict53 = {11: "up", 12: "up", 15: "upright", 16: "upright",
                  21: "up", 22: "up", 25: "upright", 26: "upright",
                  31: "up", 32: "up", 33: "up", 34: "upright", 35: "upright", 36: "upright",
                  43: "up", 44: "upright",
                  54: "right",
                  61: "down", 62: "down", 63: "down", 64: "downright", 65: "downright", 66: "downright",
                  71: "down", 72: "down", 75: "downright", 76: "downright",
                  81: "down", 82: "down", 85: "downright", 86: "downright"}
    _dir_dict54 = {11: "upleft", 12: "upleft", 15: "up", 16: "up",
                  21: "upleft", 22: "upleft", 25: "up", 26: "up",
                  31: "upleft", 32: "upleft", 33: "upleft", 34: "up", 35: "up", 36: "up",
                  43: "upleft", 44: "up",
                  53: "left",
                  61: "downleft", 62: "downleft", 63: "downleft", 64: "down", 65: "down", 66: "down",
                  71: "downleft", 72: "downleft", 75: "down", 76: "down",
                  81: "downleft", 82: "downleft", 85: "down", 86: "down"}

    _dir_dict61 = {11: "right", 12: "right", 15: "right", 16: "right",
                  21: "right", 22: "right", 25: "right", 26: "right",
                  31: "right", 32: "right", 33: "right", 34: "right", 35: "right", 36: "right",
                  43: "right", 44: "right",
                  53: "right", 54: "right",
                  62: "right", 63: "right", 64: "right", 65: "right", 66: "right",
                  71: "down", 72: "downright", 75: "right", 76: "right",
                  81: "down", 82: "downright", 85: "right", 86: "right"}
    _dir_dict62 = {11: "right", 12: "right", 15: "right", 16: "right",
                  21: "right", 22: "right", 25: "right", 26: "right",
                  31: "right", 32: "right", 33: "right", 34: "right", 35: "right", 36: "right",
                  43: "right", 44: "right",
                  53: "right", 54: "right",
                  61: "left", 63: "right", 64: "right", 65: "right", 66: "right",
                  71: "downleft", 72: "down", 75: "right", 76: "right",
                  81: "downleft", 82: "down", 85: "right", 86: "right"}
    _dir_dict63 = {11: "up", 12: "up", 15: "upright", 16: "upright",
                  21: "up", 22: "up", 25: "upright", 26: "upright",
                  31: "up", 32: "up", 33: "up", 34: "upright", 35: "upright", 36: "upright",
                  43: "up", 44: "upright",
                  53: "up", 54: "upright",
                  61: "left", 62: "left", 64: "right", 65: "right", 66: "right",
                  71: "left", 72: "left", 75: "right", 76: "right",
                  81: "left", 82: "left", 85: "right", 86: "right"}
    _dir_dict64 = {11: "upleft", 12: "upleft", 15: "up", 16: "up",
                  21: "upleft", 22: "upleft", 25: "up", 26: "up",
                  31: "upleft", 32: "upleft", 33: "upleft", 34: "up", 35: "up", 36: "up",
                  43: "upleft", 44: "up",
                  53: "upleft", 54: "up",
                  61: "left", 62: "left", 63: "left", 65: "right", 66: "right",
                  71: "left", 72: "left", 75: "right", 76: "right",
                  81: "left", 82: "left", 85: "right", 86: "right"}
    _dir_dict65 = {11: "left", 12: "left", 15: "left", 16: "left",
                  21: "left", 22: "left", 25: "left", 26: "left",
                  31: "left", 32: "left", 33: "left", 34: "left", 35: "left", 36: "left",
                  43: "left", 44: "left",
                  53: "left", 54: "left",
                  61: "left", 62: "left", 63: "left", 64: "left", 66: "right",
                  71: "left", 72: "left", 75: "down", 76: "downright",
                  81: "left", 82: "left", 85: "down", 86: "downright"}
    _dir_dict66 = {11: "left", 12: "left", 15: "left", 16: "left",
                  21: "left", 22: "left", 25: "left", 26: "left",
                  31: "left", 32: "left", 33: "left", 34: "left", 35: "left", 36: "left",
                  43: "left", 44: "left",
                  53: "left", 54: "left",
                  61: "left", 62: "left", 63: "left", 64: "left", 65: "left",
                  71: "left", 72: "left", 75: "downleft", 76: "down",
                  81: "left", 82: "left", 85: "downleft", 86: "down"}

    _dir_dict71 = {11: "upright", 12: "upright", 15: "upright", 16: "upright",
                  21: "upright", 22: "upright", 25: "upright", 26: "upright",
                  31: "upright", 32: "upright", 33: "upright", 34: "upright", 35: "upright", 36: "upright",
                  43: "upright", 44: "upright",
                  53: "upright", 54: "upright",
                  61: "up", 62: "upright", 63: "upright", 64: "upright", 65: "upright", 66: "upright",
                  72: "right", 75: "upright", 76: "upright",
                  81: "down", 82: "downright", 85: "upright", 86: "upright"}
    _dir_dict72 = {11: "up", 12: "up", 15: "up", 16: "up",
                  21: "up", 22: "up", 25: "up", 26: "up",
                  31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                  43: "up", 44: "up",
                  53: "up", 54: "up",
                  61: "upleft", 62: "up", 63: "up", 64: "up", 65: "up", 66: "up",
                  71: "left", 75: "up", 76: "up",
                  81: "downleft", 82: "down", 85: "up", 86: "up"}
    _dir_dict75 = {11: "up", 12: "up", 15: "up", 16: "up",
                  21: "up", 22: "up", 25: "up", 26: "up",
                  31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                  43: "up", 44: "up",
                  53: "up", 54: "up",
                  61: "up", 62: "up", 63: "up", 64: "up", 65: "up", 66: "upright",
                  71: "up", 72: "up", 76: "right",
                  81: "up", 82: "up", 85: "down", 86: "downright"}
    _dir_dict76 = {11: "upleft", 12: "upleft", 15: "upleft", 16: "upleft",
                  21: "upleft", 22: "upleft", 25: "upleft", 26: "upleft",
                  31: "upleft", 32: "upleft", 33: "upleft", 34: "upleft", 35: "upleft", 36: "upleft",
                  43: "upleft", 44: "upleft",
                  53: "upleft", 54: "upleft",
                  61: "upleft", 62: "upleft", 63: "upleft", 64: "upleft", 65: "upleft", 66: "up",
                  71: "upleft", 72: "upleft", 75: "left",
                  81: "upleft", 82: "upleft", 85: "downleft", 86: "down"}

    _dir_dict81 = {11: "upright", 12: "upright", 15: "upright", 16: "upright",
                  21: "upright", 22: "upright", 25: "upright", 26: "upright",
                  31: "upright", 32: "upright", 33: "upright", 34: "upright", 35: "upright", 36: "upright",
                  43: "upright", 44: "upright",
                  53: "upright", 54: "upright",
                  61: "up", 62: "upright", 63: "upright", 64: "upright", 65: "upright", 66: "upright",
                  71: "up", 72: "upright", 75: "upright", 76: "upright",
                  82: "right", 85: "upright", 86: "upright"}
    _dir_dict82 = {11: "up", 12: "up", 15: "up", 16: "up",
                  21: "up", 22: "up", 25: "up", 26: "up",
                  31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                  43: "up", 44: "up",
                  53: "up", 54: "up",
                  61: "upleft", 62: "up", 63: "up", 64: "up", 65: "up", 66: "up",
                  71: "upleft", 72: "up", 75: "up", 76: "up",
                  81: "left", 85: "up", 86: "up"}
    _dir_dict85 = {11: "up", 12: "up", 15: "up", 16: "up",
                  21: "up", 22: "up", 25: "up", 26: "up",
                  31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                  43: "up", 44: "up",
                  53: "up", 54: "up",
                  61: "up", 62: "up", 63: "up", 64: "up", 65: "up", 66: "upright",
                  71: "up", 72: "up", 75: "up", 76: "upright",
                  81: "up", 82: "up", 86: "right"}
    _dir_dict86 = {11: "upleft", 12: "upleft", 15: "upleft", 16: "upleft",
                  21: "upleft", 22: "upleft", 25: "upleft", 26: "upleft",
                  31: "upleft", 32: "upleft", 33: "upleft", 34: "upleft", 35: "upleft", 36: "upleft",
                  43: "upleft", 44: "upleft",
                  53: "upleft", 54: "upleft",
                  61: "upleft", 62: "upleft", 63: "upleft", 64: "upleft", 65: "upleft", 66: "up",
                  71: "upleft", 72: "upleft", 75: "upleft", 76: "up",
                  81: "upleft", 82: "upleft", 85: "left"}


    dir_match_direction = {11: _dir_dict11, 12: _dir_dict12, 15: _dir_dict15, 16: _dir_dict16,
                           21: _dir_dict21, 22: _dir_dict22, 25: _dir_dict25, 26: _dir_dict26,
                           31: _dir_dict31, 32: _dir_dict32, 33: _dir_dict33, 34: _dir_dict34, 35: _dir_dict35, 36: _dir_dict36,
                           43: _dir_dict43, 44: _dir_dict44,
                           53: _dir_dict53, 54: _dir_dict54,
                           61: _dir_dict61, 62: _dir_dict62, 63: _dir_dict63, 64: _dir_dict64, 65: _dir_dict65, 66: _dir_dict66,
                           71: _dir_dict71, 72: _dir_dict72, 75: _dir_dict75, 76: _dir_dict76,
                           81: _dir_dict81, 82: _dir_dict82, 85: _dir_dict85, 86: _dir_dict86}

    dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                  "right": Vector2(1,0), "down": Vector2(0,1),
                  "upleft": Vector2(1,0).rotate(225), "upright": Vector2(1,0).rotate(315),
                  "downleft": Vector2(1,0).rotate(135), "downright": Vector2(1,0).rotate(45)}

    _close_to_11 = [11, 12, 21, 22, 31, 32]
    _close_to_12 = [12, 11, 21, 22, 31, 32]
    _close_to_15 = [15, 16, 25, 26, 35, 36]
    _close_to_16 = [16, 15, 25, 26, 35, 36]

    _close_to_21 = [21, 22, 11, 12, 31, 32]
    _close_to_22 = [22, 21, 11, 12, 31, 32]
    _close_to_25 = [25, 26, 15, 16, 35, 36]
    _close_to_26 = [26, 25, 15, 16, 35, 36]

    _close_to_31 = [31, 32, 11, 12, 21, 22]
    _close_to_32 = [32, 31, 11, 12, 21, 22, 33]
    _close_to_33 = [33, 34, 43, 44, 53, 54, 63, 64, 32]
    _close_to_34 = [34, 33, 43, 44, 53, 54, 63, 64, 35]
    _close_to_35 = [35, 36, 15, 16, 25, 26, 43]
    _close_to_36 = [36, 35, 15, 16, 25, 26]

    _close_to_43 = [43, 44, 33, 34, 53, 54, 63, 64]
    _close_to_44 = [44, 43, 33, 34, 53, 54, 63, 64]

    _close_to_53 = [53, 54, 33, 34, 43, 44, 63, 64]
    _close_to_54 = [54, 53, 33, 34, 43, 44, 63, 64]

    _close_to_61 = [61, 62, 71, 72, 81, 82]
    _close_to_62 = [62, 61, 71, 72, 81, 82, 63]
    _close_to_63 = [63, 64, 33, 34, 53, 54, 43, 44, 62]
    _close_to_64 = [64, 63, 33, 34, 53, 54, 43, 44, 65]
    _close_to_65 = [65, 66, 75, 76, 85, 86, 64]
    _close_to_66 = [66, 65, 75, 76, 85, 86]

    _close_to_71 = [71, 72, 61, 62, 81, 82]
    _close_to_72 = [72, 71, 61, 62, 81, 82]
    _close_to_75 = [75, 76, 65, 66, 85, 86]
    _close_to_76 = [76, 75, 65, 66, 85, 86]

    _close_to_81 = [81, 82, 61, 62, 71, 72]
    _close_to_82 = [82, 81, 61, 62, 71, 72]
    _close_to_85 = [85, 86, 65, 66, 75, 76]
    _close_to_86 = [86, 85, 65, 66, 75, 76]

    dir_match_close_sectors = {11: _close_to_11, 12: _close_to_12, 15: _close_to_15, 16: _close_to_16,
                               21: _close_to_21, 22: _close_to_22, 25: _close_to_25, 26: _close_to_26,
                               31: _close_to_31, 32: _close_to_32, 33: _close_to_33, 34: _close_to_34, 35: _close_to_35, 36: _close_to_36,
                               43: _close_to_43, 44: _close_to_44,
                               53: _close_to_53, 54: _close_to_54,
                               61: _close_to_61, 62: _close_to_62, 63: _close_to_63, 64: _close_to_64, 65: _close_to_65, 66: _close_to_66,
                               71: _close_to_71, 72: _close_to_72, 75: _close_to_75, 76: _close_to_76,
                               81: _close_to_81, 82: _close_to_82, 85: _close_to_85, 86: _close_to_86}
