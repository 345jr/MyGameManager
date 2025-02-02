from nicegui import ui ,run
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import selenium.webdriver as webdriver


from shared import *
import time


result = None
seacher_list = []
loading_text = False
loading_gif = False
on_download = False

def get_input(e):
    global input_value
    input_value = e.value


async def get_submit():
    global result
    global loading_text
    global loading_gif
    global seacher_list
    global on_download
    seacher_list.clear() 
    dialog = ui.dialog()
    with dialog, ui.card():
        with ui.column():
            ui.label("搜索结果" )
            loading_text =  ui.label("请稍后...(这个过程可能稍久)").classes("text-lg text-bold")
            on_download = ui.label("正在获取与下载中......").classes("text-lg text-bold")
            loading_gif = ui.image("examples/loading.gif")
            result = ui.column()
    on_download.visible = False
    dialog.open()
    seacher_list = await run.io_bound(get_torrent , input_value)
    loading_text.visible = False
    loading_gif.visible = False
    for j , i  in enumerate(seacher_list):
        with result:
            with ui.card().classes("flex items-center gap-4 p-4 flex-row"):
                ui.image(i["img"]).classes("w-24 h-24 object-cover rounded")
                with ui.column().classes("flex-1"):
                    ui.label(f"游戏名: {i['name']}").classes("font-semibold text-lg")
                    ui.label(f"发行年份: {i['release']}")
                    ui.label(f"大小: {i['size']}")
                ui.button("一键下载" , on_click=lambda index = j , dialog =dialog  : select_search(index , dialog)).classes("ml-auto")
    
    
async def select_search(index , dialog):
    result.visible = False
    loading_text.visible = False
    on_download.visible = True
    loading_gif.visible = True 
    tip = await run.io_bound(get_torrent_real , index)
    dialog.close()
    loading_text.visible = False
    loading_gif.visible = False
    ui.notify(tip)


def get_torrent(input_value):
    print("爬虫已启动")
    chrome_options = Options()
    chrome_service = Service(executable_path="driver/chromedriver.exe")
    chrome_options.add_argument('--headless')
    url = "https://byrutgame.org/"
    driver = webdriver.Chrome(service=chrome_service , options=chrome_options)
    try:
        driver.get(url)
        searcher_box = WebDriverWait(driver , 10).until(
            EC.presence_of_element_located((By.ID, "story"))
        )
        searcher_box.clear()
        searcher_box.send_keys(input_value)
        searcher_box.send_keys(Keys.ENTER)
        result = driver.page_source
        soup = BeautifulSoup( result, 'lxml')        
        seacher_list_result = soup.find_all(name="a" , attrs={"class":"search_res"} )
        for i in seacher_list_result:
            game_name = i.find(name="div" , attrs={"class":"search_res_title"})
            game_info = i.find_all(name ="div" , attrs={"class":"search_res_sub"})
            spans = game_info[0].find_all(name="span")
            if len(spans) >= 2:
                game_release = spans[0].text
                game_size = spans[1].text
                game_size = game_size.replace("ГБ", "GB").replace("МБ", "MB")  
            game_img = i.find(name="img")
            img_url = url + game_img['src']
            seacher_list.append({"name":game_name.text,"release":game_release ,"size":game_size ,"img":img_url})         
    finally:
        driver.quit()
    return seacher_list

def get_torrent_real(index):
    print("爬虫已启动")
    chrome_options = Options()
    chrome_service = Service(executable_path="driver/chromedriver.exe")
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": r"C:\Galgame\MyGameManager\torrent",
        "download.prompt_for_download": False,  
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,  
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.automatic_downloads": 1 ,
        "images": 2 ,
        "stylesheets": 2 
    })
    url = "https://byrutgame.org/"
    driver = webdriver.Chrome(service=chrome_service , options=chrome_options)
    try:
        driver.get(url)
        searcher_box = WebDriverWait(driver , 10).until(
            EC.presence_of_element_located((By.ID, "story"))
        )
        searcher_box.send_keys(input_value)
        searcher_box.send_keys(Keys.ENTER)
        a_result = driver.find_elements(By.CLASS_NAME, "search_res")
        for i , j  in enumerate(a_result):
            if index == i :
                j.click()
        a_result = driver.find_element(By.CLASS_NAME, "itemtop_games")
        driver.execute_script("arguments[0].click();" , a_result)
    finally:
        time.sleep(5)
        print("已完成第二流程")
        tip = "下载成功✨ !"
        driver.quit()
    return tip


async def network_test():
    url1 ="https://www.baidu.com"
    url2 = "https://byrutgame.org/"
    timeout = 15
    with ui.dialog() as dialog , ui.card():
        with ui.column():
            ui.label("网络测试")
            test_result1 = ui.column()
            test_result2 = ui.column()
    dialog.open()    
    test1 =  await run.io_bound(get_test_result , url1 ,timeout)   
    test2 =  await run.io_bound(get_test_result , url2 ,timeout)
    if test1["status_code"] == test2["status_code"]:
        ui.notify("网络正常 , 你可以正常地爬取资源😁")
    else:
        ui.notify("网络异常 , 你需要解决这两个网站的访问问题😭")
    with test_result1 :
        ui.label(f"网址 :{test1['url']}  访问状态 :{test1['status']}  状态码 :{test1['status_code']}")    
    with test_result2 :
        ui.label(f"网址 :{test2['url']}  访问状态 :{test2['status']}  状态码 :{test2['status_code']}")        
    
    
        
    

def get_test_result(url ,timeout):
    try:
        response = requests.get(url, timeout=timeout , stream=True , allow_redirects=True , headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/58.0.3029.110 Safari/537.3"
        })
        
        if response.status_code == 200:
            return {"url": url, "status": "成功", "status_code": response.status_code}
        else:
            return {"url": url, "status": "失败", "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"url": url, "status": "失败", "error": str(e)}
    

def help():
    with ui.dialog() as dialog , ui.card():
        with ui.column():
            ui.label("如果你需要找一款游戏到能玩上它的流程如下").classes("text-xl")
            ui.label("0.知道这个游戏的中文名")
            ui.label("->1.根据中文名去搜索这个游戏的英文名")
            ui.label("->2.可去steamDB上搜索，检查该英文名是否准确")
            ui.label("->3.通过该英文名直接爬取，并下载种子即可")
            ui.label("->4.通过夸克网盘或者其他的平台下载该种子，并且安装游戏(如果需要安装)")
            ui.label("->5.将其放入game-box，扫描添加启动程序，即可更加便捷地管理和启动游戏(当然你不放也行，都是能玩的)")
            ui.link('找游戏->SteamDB,快速查找游戏，包含所有steam的游戏', 'https://steamdb.info/' , new_tab=True)
            ui.label("")
    dialog.open()