import requests
url = "https://byrutgame.org/"
def get_test_result(url ,timeout):
    try:
        response = requests.get(url, timeout=timeout ,stream=True, allow_redirects=True,headers={
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
print(get_test_result(url , 15))