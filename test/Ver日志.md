

## 版本v0.0.1

我以一个初学者的水平完成了这个游戏管理器，有添加游戏和启动游戏的功能

```python
import subprocess

def add_game():
    with open('my_game_date.txt','r') as f:
        lines = f.readlines()
        if not lines :
            number =  0       
        else:
            for line in lines:
                data = line.rstrip()
                number,game_name,game_address = data.split('|')
    with open('my_game_date.txt','a') as f:
            number = str(int(number) + 1)
            game_name = input('请输入游戏名字 :')
            game_address= input('请输入游戏地址 :')
            f.write(number+'|'+game_name+'|'+game_address+'\n')

def selet_game():
    game_address_all = []
    with open('my_game_date.txt','r') as f:
        lines = f.readlines()
        if not lines :
            number =  1       
        else:
            for line in lines:
                data = line.rstrip()
                number,game_name,game_address = data.split('|')
                print(data)
                game_address_all.append(game_address)
    launch(game_address_all)

def launch(game_address_all):
    result = int(input('请选择你要开启的游戏 :(输入游戏序号) '))
    address_dict = {index: address for index , address in enumerate(game_address_all)}
    subprocess.run(address_dict[result-1])

def main ():
    while True:
        option = input("1.添加游戏\n2.启动游戏\n3.退出\n(请输入数字选择) ")
        if option == '1':
            add_game()
        if option == '2':
            selet_game()
        if option =='3':
            quit()
main()
```

下一个计划:

- [x] 添加删除游戏的功能


- [x] 优化代码


- [x] 添加记录时间的功能，在启动游戏中可以查看每一个游戏的已运行时间(格式大概是---100.5小时<-例子) 




## 版本v0.0.2



修改了数据结构，从txt存储转到JSON存储

添加了记录游戏时间的功能.

添加了预览功能

添加了删除功能

添加了rich print模块，单纯为了打印好看一点。

所有功能基本正常

BUG:(当以谷歌浏览器作为测试对象时，会发生计算时间不准的的问题，)

GPT解释:当你使用 `subprocess.run()` 或 `subprocess.Popen()` 来启动一个图形化应用程序（例如 Google Chrome），这种应用程序通常会立即返回控制权给操作系统，而不等待用户关闭窗口。这是因为图形化应用程序通常是异步启动的：一旦它们启动，控制权就立即返回给调用程序，而不是等到应用程序关闭后才返回。

```python
import subprocess
import json
import pprint
from rich import print
import time


def add_game_json():
    with open("game_records.json", "r") as f:
        try:
            original_game_datas = json.load(f)  # 先读取已有内容
        except json.JSONDecodeError:
            original_game_datas = []
    a_uid = 1
    for i in original_game_datas:
        a_uid = i["UID"] + 1

    game_n = input("请输入游戏名字 :")
    game_a = input("请输入游戏地址 :")
    game_t = 0
    new_UID = a_uid
    new_data = {"UID": new_UID, "name": game_n, "address": game_a, "time": game_t}
    original_game_datas.append(new_data)  # 添加新内容后重写
    game_data = json.dumps(original_game_datas, ensure_ascii=False, indent=4)
    with open("game_records.json", "w") as f:
        f.write(game_data)


def delete_game_json():
    with open("game_records.json", "r") as f:
        original_game_datas = json.load(f)
        for i in original_game_datas:
            print(i)
        your_delete_num = int(input("请输入你需要删除的游戏UID "))
        # 通过列表推导式来过滤达到删除的效果:D
        original_game_datas = [
            i for i in original_game_datas if i["UID"] != your_delete_num
        ]
        new_game_datas = json.dumps(original_game_datas, ensure_ascii=False, indent=4)
        with open("game_records.json", "w") as f:
            f.write(new_game_datas)


def selet_game_json():
    with open("game_records.json", "r") as f:
        original_game_datas = json.load(f)
        uid_address = {}
        for i in original_game_datas:
            uid = i["UID"]
            address = i["address"]
            uid_address[uid] = address
        launch_game(uid_address)


def launch_game(uid_address):
    this_run_time = 0
    for i, j in uid_address.items():
        i = str(i)
        print(i + "|" + j)
    result = input("请选择你要开启的游戏 :(输入游戏序号) ")
    for i, j in uid_address.items():
        i = str(i)
        if result == i:
            start_time = time.time()
            subprocess.run(j)
            run_time = time.time() - start_time
            this_run_time = run_time
    record_time(this_run_time, result)


def record_time(this_run_time, result):
    # 重写时间
    with open("game_records.json", "r") as f:
        try:
            original_game_datas = json.load(f)
        except json.JSONDecodeError:
            original_game_datas = []
        target_uid = int(result)
        for i in original_game_datas:
            if i["UID"] == target_uid:
                i["time"] += this_run_time
    game_data = json.dumps(original_game_datas, ensure_ascii=False, indent=4)
    with open("game_records.json", "w") as f:
        f.write(game_data)


def preview():
    with open("game_records.json", "r") as f:
        try:
            original_game_datas = json.load(f)
        except json.JSONDecodeError:
            original_game_datas = []
        # 格式化时间
        for i in original_game_datas:
            hou = round(i["time"] // 3600)
            min = round((i["time"] % 3600) // 60)
            sed = round(i["time"] % 3600)
            a_time = f"{hou}时{min}分钟{sed}秒"
            i["time"] = a_time
        print(original_game_datas)


def main():
    while True:
        print("----------")
        option = input(
            "1.管理游戏\n2.启动游戏\n3.预览\n4.退出\n(请输入数字选择)\n----------\n"
        )
        if option == "1":
            option2 = input("1.添加游戏\n2.删除游戏\n")
            if option2 == "1":
                add_game_json()
            elif option2 == "2":
                delete_game_json()
            else:
                continue
        if option == "2":
            selet_game_json()
        if option == "3":
            preview()
        if option == "4":
            quit()


main()

```

下一个计划

- [x] 优化代码,减少冗余:

  通过方法减少了一部分重复的代码

  

UID 逻辑漏洞BUG

更改为面向对象的设计模式

记录时间的优化(及修复类似于谷歌浏览器这样的BUG)

更好的数据展示

## Ver0.0.5

- [x] 使用nicegui开发了可交互的页面（tailwindCSS的部分使用）
- [x] 修复了时间秒数错误的bug
- [x] 添加了扫描添加的游戏的功能，提升了智能性
- [x] 分离了部分ui的代码，完善了结构性
- [x] 完成了在每一个游戏内部的卡片的开始游戏，详细页，删除游戏
- [x] 添加了图片上传功能，可以自由地替换每一个游戏卡片的背景图。
- [x] 加入了扫描黑名单，以及移除相关扫描黑名单的功能
- [x] 解决了关闭窗口和关闭服务的功能
- [x] 解决了响应式更新的问题
- [x] 加入了游戏大小这一指标
- [x] 完成了3个基础排序，游戏时间，启动时间，游戏大小
- [x] 完成了搜索功能
- [x] 完成了打开游戏仓库文件夹的功能
- [x] 完成了对git的整合，可以上传游戏到git仓库