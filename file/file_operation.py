import os
import subprocess
from nicegui import ui

#因为可能存在文件夹套文件夹的问题，需要多次递归。避免4096
def get_size(path):
    size = 0
    for i in os.scandir(path):
        if i.is_file():
            size += os.stat(i).st_size
        elif i.is_dir():
            size += get_size(i)
    return size

def open_folder(path):
    try:
        subprocess.run(['explorer', path] , check=False)
    except subprocess.CalledProcessError:
        ui.notify('打开失败', type='negative')