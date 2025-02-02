from my_ui import *

cpwd = Path(__file__).parent
game_box_path = cpwd.parent / "game-box"
image_path = cpwd / "image"
driver_path = cpwd / "driver"
if not game_box_path.exists():
    #parents：如果父目录不存在，是否创建父目录。exist_ok：只有在目录不存在时创建目录，目录已存在时不会抛出异常
    game_box_path.mkdir(parents=True, exist_ok=True)
    image_path.mkdir(parents=True, exist_ok=True)
    driver_path.mkdir(parents=True, exist_ok=True)
else:
    pass

ui.add_head_html('''
    <style>
        body {
            background-image: url('/examples/background.jpg');
            background-size: cover;
            background-position: center;   
        }
    </style>
    ''')


async def on_shutdown():
    pass
app.on_shutdown(on_shutdown)
app.native.window_args['min_size'] = (1120, 650)
app.native.window_args['resizable'] = True
app.add_static_files('/examples', 'examples')

ui.run(native=True,
       window_size=(1120, 650),
       title="游戏仓库",
       favicon="examples/favicon.ico",
       reload=False)
