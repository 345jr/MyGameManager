import subprocess
import time
import json
from pathlib import Path
from nicegui import ui, events , app

import shared
from file import file_operation, read_or_write



UPLOAD_FOLDER = Path("./image")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
UUID = 0
UNAME = ''


async def add_game():
    with ui.dialog() as dialog, ui.card():
        ui.label("添加新游戏")
        game_name = ui.input("游戏名字")
        game_address = ui.input("游戏地址")

        async def handle_submit():
            if game_name.value and game_address.value:
                original_game_datas = read_or_write.read_file()
                a_uid = 1
                if original_game_datas:
                    a_uid = max(item["UID"]
                                for item in original_game_datas) + 1
                new_data = {
                    "UID": a_uid,
                    "name": game_name.value,
                    "address": game_address.value,
                    "time": 0,
                    "last_time": 0,
                    "size": 0
                }
                original_game_datas.append(new_data)
                read_or_write.write_file(original_game_datas)
                dialog.close()
                # 刷新一下
                preview()

        with ui.row():
            ui.button("确定", on_click=handle_submit)
            ui.button("取消", on_click=dialog.close)
    dialog.open()


async def quick_add(exe_file, game_size):
    with ui.dialog() as dialog, ui.card():
        ui.label("添加新游戏")
        game_name = ui.input("游戏名字")

        async def handle_submit():
            if game_name.value and exe_file:
                original_game_datas = read_or_write.read_file()
                a_uid = 1
                if original_game_datas:
                    a_uid = max(item["UID"]
                                for item in original_game_datas) + 1
                new_data = {
                    "UID": a_uid,
                    "name": game_name.value,
                    "address": exe_file,
                    "time": 0,
                    "last_time": 0,
                    "size": game_size
                }
                original_game_datas.append(new_data)
                read_or_write.write_file(original_game_datas)
                dialog.close()
                # 刷新一下
                preview()

        with ui.row():
            ui.button("确定", on_click=handle_submit)
            ui.button("取消", on_click=dialog.close)
    dialog.open()


async def delete_game():
    with ui.dialog() as dialog, ui.card():
        ui.label("删除游戏")
        your_delete_num = ui.input("请输入你需要删除的游戏UID ")

        async def handle_submit():
            delete_num = int(your_delete_num.value)
            # 通过列表推导式来过滤达到删除的效果:D
            original_game_datas = [
                i for i in read_or_write.read_file() if i["UID"] != delete_num
            ]
            read_or_write.write_file(original_game_datas)
            dialog.close()
            # 刷新一下
            preview()

        with ui.row():
            ui.button("确定", on_click=handle_submit)
            ui.button("取消", on_click=dialog.close)
    dialog.open()


async def selet_game():
    original_game_datas = read_or_write.read_file()

    with ui.dialog() as dialog, ui.card():
        ui.label("启动游戏")
        result = ui.input("请输入你需要启动的游戏UID ")

        async def handle_submit():
            dialog.close()
            new_result = int(result.value)
            try:
                a_address = next(i["address"] for i in original_game_datas
                                 if i["UID"] == new_result)
                start_time = time.time()
                subprocess.run(a_address)
                run_time = time.time() - start_time
                record_time(run_time, new_result, start_time)
                preview()
            except StopIteration:
                ui.notify("没有这个游戏", close_button="OK")

        with ui.row():
            ui.button("确定", on_click=handle_submit)
            ui.button("取消", on_click=dialog.close)
    dialog.open()


async def quick_start(dict_of_game):
    start_time = time.time()
    subprocess.run(dict_of_game["address"])
    run_time = time.time() - start_time
    record_time(run_time, dict_of_game["UID"], start_time)


async def quick_delete(dict_of_game):
    your_delete_num = dict_of_game["UID"]
    original_game_datas = read_or_write.read_file()
    for i in original_game_datas:
        if i["UID"] == your_delete_num:
            original_game_datas.remove(i)
    read_or_write.write_file(original_game_datas)
    preview()


async def quick_preview(dict_of_game):
    with ui.dialog() as dialog, ui.card():
        ui.label("详细信息").classes("text-xl")
        ui.label("游戏地址:")
        ui.label(dict_of_game["address"])
        ui.label("上一次启动时间:")
        try:
            ui.label(
                time.strftime("%Y-%m-%d",
                              time.localtime(dict_of_game["last_time"])))
            ui.label("游戏大小 :")
            ui.label(f"{dict_of_game['size']/(1024**3):.2f} GB")
        except KeyError:
            ui.label("不存在")
    dialog.open()


async def quick_image(dict_of_game):
    global UUID
    global UNAME
    UUID = dict_of_game["UID"]
    UNAME = dict_of_game["name"]
    with ui.dialog() as dialog, ui.card():
        ui.upload(
            label="上传图片",
            auto_upload=True,
            on_upload=handle_upload,
        )
    dialog.open()


def handle_upload(e: events.UploadEventArguments):
    global UUID
    UUID = str(UUID)
    b = e.content.read()
    file_name = e.name
    file_extension = Path(file_name).suffix
    new_file_name = f"{UUID}_{UNAME}{file_extension}"
    save_path = Path("./image") / new_file_name
    save_path.write_bytes(b)
    preview()


def record_time(this_run_time, result, start_time):
    # 重写时间
    original_game_datas = read_or_write.read_file()
    target_uid = int(result)
    for i in original_game_datas:
        if i["UID"] == target_uid:
            i["time"] += this_run_time
            i["last_time"] = start_time
    read_or_write.write_file(original_game_datas)


def preview():
    original_game_datas_sort = read_or_write.read_file()
    game_list(original_game_datas_sort)


async def blacklist():
    with ui.dialog() as dialog, ui.card():
        with ui.row():
            ui.label("已扫描列表 :").classes("text-xl mt-1")
        blacklist = read_or_write.read_notFile()
        black_container = ui.column()
        for i in blacklist:
            with black_container:
                ui.button("移除",
                          icon="arrow_downward",
                          color="red",
                          on_click=lambda i=i, black_container=black_container:
                          out_blacklist(i, black_container))
                ui.label(i).classes("underline text-lg")
        ui.button(
            "一键清空",
            icon="delete_forever",
            color="red",
            on_click=lambda black_container=black_container: clear_blacklist(
                black_container)).classes("absolute right-5 top-5")
    dialog.open()


async def out_blacklist(i, black_container):
    alreadyAddress = read_or_write.read_notFile()
    for j in alreadyAddress:
        if j == i:
            alreadyAddress.remove(j)
    read_or_write.write_notFile(alreadyAddress)
    blacklist = read_or_write.read_notFile()
    ui.notify("移除成功")
    black_container.clear()
    for i in blacklist:
        with black_container:
            ui.button("移除",
                      icon="arrow_downward",
                      color="red",
                      on_click=lambda i=i, black_container=black_container:
                      out_blacklist(i, black_container))
            ui.label(i).classes("underline")


async def clear_blacklist(black_container):
    clear_black_list = []
    with open("data/notIsgame.json", "w", encoding="utf-8") as f:
        json.dump(clear_black_list, f, ensure_ascii=False, indent=4)
    ui.notify("已清空")
    black_container.clear()


def checking():
    original_game_datas = read_or_write.read_file()
    alreadyAddress = read_or_write.read_notFile()
    pos = Path("../game-box").resolve()
    scan_num = 0
    with ui.dialog() as dialog, ui.card():
        with ui.row():
            ui.label("扫描结果 :").classes("text-xl")
            show_folders = ui.switch("显示文件夹", value=False)
            show_exe = ui.switch("显示可执行文件", value=True)
        for i in pos.iterdir():

            if i.is_dir():
                ui.label(f"{i.name}").classes(
                    "text-basefont-bold text-yellow-500").bind_visibility_from(
                        show_folders, "value")
                scan_num += 1
            exe_file = list(i.rglob("*.exe"))
            for j in exe_file:
                exe_file = str(j)
                #避免重复扫描
                if exe_file not in alreadyAddress:
                    game_size = file_operation.get_size(i)
                    with ui.column().classes("gap-y-4"):
                        #设置回调函数时需要一个可调用的对象，如果不用lambda会发生错误，系统认为会直接执行该函数
                        ui.button(
                            "添加",
                            icon="arrow_downward",
                            color="green",
                            on_click=lambda exe_file=exe_file, game_size=
                            game_size: quick_add(exe_file, game_size)).classes(
                                "rounded-full ")
                        ui.label(f"{exe_file}").classes(
                            "").bind_visibility_from(show_exe, "value")
                        alreadyAddress.append(exe_file)
                        read_or_write.write_notFile(alreadyAddress)
        ui.label(f"扫描已完成，扫描了{scan_num}个文件夹")
        ui.button("已扫描名单", on_click=blacklist)
    dialog.open()


def game_list(sort_method):
    view_game = shared.view_game
    view_game.clear()
    for i in sort_method:
        hou = round(i["time"] // 3600)
        min = round((i["time"] % 3600) // 60)
        sed = round(i["time"] % 60)
        a_time = f"{hou}小时{min}分钟{sed}秒"
        i["time"] = a_time
        with view_game:
            with ui.card().classes("flex-row").classes(
                    "pr-0 pt-0 pb-0 bg-slate-600"):
                with ui.column().classes("flex w-52 pt-4 "):
                    ui.label(f"UID :{i['UID']}").classes("text-lime-500")
                    ui.label("游戏名字").classes(
                        "text-xs italic font-bold text-white")
                    ui.label(f"{i['name']}").classes(
                        "text-base text-yellow-400")
                    ui.label(f"游戏时间 ").classes(
                        "text-xs italic font-bold text-white")
                    ui.label(f"{i['time']}").classes("text-lime-500")
                with ui.column().classes("pt-4 "):
                    ui.button(
                        "启动游戏",
                        icon="rocket_launch",
                        color="green",
                        on_click=lambda i=i: quick_start(i),
                    ).classes("w-32 font-black text-white")
                    ui.button(
                        "详细",
                        icon="info_outline",
                        on_click=lambda i=i: quick_preview(i),
                    ).classes("w-32 font-black text-white")
                    ui.button(
                        "删除",
                        icon="delete",
                        color="red",
                        on_click=lambda i=i: quick_delete(i),
                    ).classes("w-32 font-black text-white")
                    with ui.row():
                        ui.button(
                            icon="image",
                            color="Plum",
                            on_click=lambda i=i: quick_image(i),
                        ).classes("w-5 text-xs ")
                        ui.button(icon="thumb_up",
                                  color="SteelBlue").classes("w-5 text-xs")
                        ui.button(icon="thumb_down",
                                  color="OrangeRed").classes("w-5 text-xs")
                pos = Path("./image").resolve()
                find_it = False
                for j in pos.iterdir():
                    image_name = j.stem
                    if image_name == f"{i['UID']}_{i['name']}":
                        find_it = True
                        game_image = f"{j.name}"
                ui.image(
                    f"image/{game_image}" if find_it else "image/0.jpg"
                ).classes(
                    "w-64 h-64 object-cover rounded-r-lg border-l-4 border-sky-400"
                )
    view_game.update()
