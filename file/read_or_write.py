import json
from pathlib import Path

FILE_PATH = Path("data/game_records.json")
FILE2_PATH = Path("data/notIsgame.json")

def read_file():
    if not FILE_PATH.exists():
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        try:
            original_game_datas = json.load(f)
        except json.JSONDecodeError:
            original_game_datas = []
    return original_game_datas


def read_notFile():
    if not FILE2_PATH.exists():
        with open(FILE2_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(FILE2_PATH, "r", encoding="utf-8") as f:
        try:
            alreadyAddress = json.load(f)
        except json.JSONDecodeError:
            alreadyAddress = []
    return alreadyAddress


def write_file(original_game_datas):
    game_data = json.dumps(original_game_datas, ensure_ascii=False, indent=4)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(game_data)


def write_notFile(alreadyAddress):
    not_data = json.dumps(alreadyAddress, ensure_ascii=False, indent=4)
    with open(FILE2_PATH, "w", encoding="utf-8") as f:
        f.write(not_data)
