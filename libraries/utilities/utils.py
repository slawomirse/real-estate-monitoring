import json
import yaml


def read_json_from_file(filepath):
    with open(filepath) as file:
        data = json.load(file)
    return data


def load_config(path: str):
    with open(path) as file:
        config = yaml.safe_load(file)
    return config


def clear_white_characters(text: str):
    return (
        text.strip()
        .replace("\n", "")
        .replace("\t", "")
        .replace("\xa0", " ")
        .replace("  ", "")
    )
