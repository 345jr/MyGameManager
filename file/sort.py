from . import read_or_write
from managerModule import game_list

from thefuzz import fuzz



def time_sort():
    original_game_datas = read_or_write.read_file()
    sorted_by_time = sorted(original_game_datas, key=lambda i: i["time"], reverse=True)
    game_list(sorted_by_time)


def last_time_sort():
    original_game_datas = read_or_write.read_file()
    sorted_by_last_time = sorted(
        original_game_datas, key=lambda i: i["last_time"], reverse=True
    )
    game_list(sorted_by_last_time)


def storage_sort():
    original_game_datas = read_or_write.read_file()
    sorted_by_last_time = sorted(
        original_game_datas, key=lambda i: i["size"], reverse=True
    )
    game_list(sorted_by_last_time)


def search_sort(your_search_word):
    original_game_datas = read_or_write.read_file()
    for i in original_game_datas:
        i["score"] = fuzz.token_sort_ratio(i["name"] , your_search_word)
    searched_sort = sorted( original_game_datas, key=lambda i: i["score"], reverse=True)
    game_list(searched_sort)

