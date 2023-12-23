from dataclasses import dataclass


@dataclass
class ConfigDifficultLevel:
    """Class for storing game parameters for different difficulty levels"""
    bot_speed: float
    bot_hitpoints: float
    bot_damage: float
    bot_attack_frequency: float
    gunpack_frequency: float
    gunpack_max_amount: int
    ammo_amount: str
    hp_restore: str

    def __getitem__(self, item):
        return getattr(self, item)


config_difficult_level_easy = ConfigDifficultLevel(
    bot_speed = 0.9,
    bot_hitpoints = 92,
    bot_damage = 18,
    bot_attack_frequency = 0.7,
    gunpack_frequency = 6,
    gunpack_max_amount = 4,
    ammo_amount = "duży",
    hp_restore = "duży",
)

config_difficult_level_medium = ConfigDifficultLevel(
    bot_speed = 1.1,
    bot_hitpoints = 100,
    bot_damage = 20,
    bot_attack_frequency = 0.55,
    gunpack_frequency = 7,
    gunpack_max_amount = 3,
    ammo_amount = "średni",
    hp_restore = "średni",
)

config_difficult_level_hard = ConfigDifficultLevel(
    bot_speed = 1.35,
    bot_hitpoints = 115,
    bot_damage = 22,
    bot_attack_frequency = 0.4,
    gunpack_frequency = 9,
    gunpack_max_amount = 3,
    ammo_amount = "niski",
    hp_restore = "niski",
)
