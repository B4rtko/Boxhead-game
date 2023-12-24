import yaml
from typing import Collection


def load_yaml(path: str) -> Collection:
    with open(path, "r") as file:
        result = yaml.load(file, Loader=yaml.Loader)
    return result
