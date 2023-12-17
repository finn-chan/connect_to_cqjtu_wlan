from json import load


def Read(path: str) -> dict:
    with open(path, 'r') as config_file:
        data = load(config_file)
        return data
