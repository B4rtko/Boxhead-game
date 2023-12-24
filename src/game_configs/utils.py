import yaml
from typing import Collection


def load_yaml(path: str) -> Collection:
    with open(path, "r") as file:
        result = yaml.load(file, Loader=yaml.Loader)
    return result


def save_yaml(path: str, data) -> None:
    with open(path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
