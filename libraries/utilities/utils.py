import json
import yaml
import os


def read_json_from_directory(directory_path: str):
    data = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            with open(file_path) as file:
                json_data = json.load(file)
                data.append(json_data)
    return [item for sublist in data for item in sublist]


def write_json_to_file(data, filename):
    with open(filename, "w", encoding="utf-8") as output:
        json.dump(data, output, ensure_ascii=False, indent=4)


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
