from managerModule import *
from file import sort
from file import crawler

PATH = Path("../game-box")
PATH_TORRENT = Path("./torrent")

with ui.element().classes("w-full flex flex-row "):
    with ui.column().classes("w-1/3 "):
        with ui.image('examples/mylogo.png').classes(
                "border-2 border-dashed border-pink-500 rounded-lg shadow-lg shadow-pink-500/50 p-4 "
        ):
            ui.label('今天玩点什么?😊').classes(
                'absolute-bottom text-subtitle2 text-center ')
        with ui.card():
            with ui.row().classes("gap-1"):
                ui.button("手动添加", icon="playlist_add", on_click=add_game)
                ui.button("扫描添加", icon="radar", on_click=checking)
                ui.button(icon="refresh", on_click=preview)
                ui.button("游戏时长", icon="sort",
                          on_click=sort.time_sort).classes("px-1")
                ui.button("最近启动", icon="sort",
                          on_click=sort.last_time_sort).classes("px-1")
                ui.button("存储大小", icon="sort",
                          on_click=sort.storage_sort).classes("px-2")
            with ui.row().classes(""):
                ui.input(label='搜索', placeholder='游戏名',
                        on_change=lambda e : sort.search_sort(e.value)).props("outlined color=primary")
                ui.button("文件夹", icon="folder", color="gold" , 
                          on_click=lambda :file_operation.open_folder(PATH)).classes("mt-2")
        with ui.column():
            with ui.card().classes():
                with ui.column().classes():
                    ui.label("🌱游戏种子🌱").classes('text-center text-2xl font-bold text-gray-800 ml-20 bg-gradient-to-r from-emerald-400 via-green-500 to-lime-500 bg-clip-text text-transparent')
                    ui.input(label="游戏名" , placeholder='请用英文搜索',on_change=crawler.get_input).classes('w-80 p-2 border border-gray-300 rounded-lg shadow-sm')
                with ui.button_group().classes("mx-0"):
                    ui.button('开始爬取', icon="pest_control", color="teal" , on_click=crawler.get_submit).classes("w-32 text-black font-bold")
                    ui.button('测试', icon="settings"  , color="green",on_click=crawler.network_test).classes("w-32 text-black font-bold")
                    with ui.button('帮助', color="lime",on_click=crawler.help).classes("w-16 text-black font-bold"):
                        ui.tooltip('使用前可以看看').classes('bg-green')
                ui.button("种子库" , color="gold" , on_click=lambda :file_operation.open_folder(PATH_TORRENT)).classes("w-80 text-black font-bold")
                with ui.timeline(side="right"):
                    ui.timeline_entry(
                        "使用nicegui开发了可交互的界面✅持续开发中",
                        title="0.0.5版本",
                        subtitle="2025.1.7",
                    )
                    ui.timeline_entry(
                        "修复了时间秒数bug✅添加了自动扫描添加游戏的方式,只需要把游戏放到仓库即可✅对pathlib模块的初次学习",
                        title="0.0.3版本",
                        subtitle="2025.1.5",
                    )
                    ui.timeline_entry(
                        "修改了数据结构,从txt存储转到JSON存储添加了记录游戏时间的功能.添加了预览功能添加了删除功能添加了rich print模块,单纯为了打印好看一点。所有功能基本正常",
                        title="0.0.2版本",
                        subtitle="2024.12",
                    )
                    ui.timeline_entry(
                        "我以一个初学者的水平完成了这个游戏管理器，有添加游戏和启动游戏的功能",
                        title="0.0.1版本",
                        subtitle="2024.12",
                        icon="rocket",
                    )
    with ui.column().classes("w-3/5  ml-4"):
        shared.view_game = ui.column()
preview()



