from flask import Flask, render_template_string
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

app = Flask(__name__)

# HTML content template (will be updated dynamically)
html_content = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Output Data</title>
</head>
<body>
    <h1>爬蟲數據</h1>
    <ul>
    {% for line in lines %}
        <li>{{ line }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

# Data to render in the HTML template
output_data = []

@app.route('/')
def index():
    global output_data
    return render_template_string(html_content, lines=output_data)

def scroll_page(driver, scroll_pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def crawl_main_page(url):
    # 設置 Selenium 的 Chrome 參數
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 使用無頭模式
    chrome_options.add_argument("--no-sandbox")  # 在無沙盒模式下運行
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免共享內存問題
    chrome_options.binary_location = "/usr/bin/google-chrome"  # 指定 Chrome 的二進制文件路徑

    # 啟動 Chrome 瀏覽器
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    main_page_data = []
    try:
        driver.get(url)
        scroll_page(driver)
        elements = driver.find_elements(By.CSS_SELECTOR, ".row.listBS")
        for element in elements:
            link_element = element.find_element(By.TAG_NAME, "a")
            href = link_element.get_attribute("href")
            main_page_data.append({"text": element.text, "href": href})
    finally:
        driver.quit()
    return main_page_data

def crawl_detail_pages(main_page_data):
    # 設置 Selenium 的 Chrome 參數
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/google-chrome"

    # 啟動 Chrome 瀏覽器
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        global output_data
        output_data = []  # Clear previous data
        for data in main_page_data:
            output_data.append(f"Q: {data['text']}")
            output_data.append(f"Link: {data['href']}")
            driver.get(data['href'])
            time.sleep(5)
            try:
                mpgdetail_element = driver.find_element(By.CSS_SELECTOR, ".mpgdetail")
                mpgdetail_text = mpgdetail_element.text
                output_data.append(f"A: {data['text']}")
                output_data.append(f"Detail: {mpgdetail_text} {data['text']}")
            except:
                output_data.append(f"A: No mpgdetail found {data['text']}")
            output_data.append("")  # Insert a blank line
    finally:
        driver.quit()

def main():
    urls = [
        "https://www.ntsh.ntpc.edu.tw/p/403-1000-41-1.php?Lang=zh-tw",
        "https://www.ntsh.ntpc.edu.tw/p/403-1000-99-1.php?Lang=zh-tw",
        "https://www.ntsh.ntpc.edu.tw/p/403-1000-38-1.php?Lang=zh-tw",
        "https://www.ntsh.ntpc.edu.tw/p/403-1000-98-1.php?Lang=zh-tw",
        "https://www.ntsh.ntpc.edu.tw/p/403-1000-95-1.php?Lang=zh-tw"
    ]

    all_main_page_data = []
    for url in urls:
        main_page_data = crawl_main_page(url)
        all_main_page_data.extend(main_page_data)
    crawl_detail_pages(all_main_page_data)

def run_flask_app():
    # 綁定 Flask 應用到正確的主機和端口
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), use_reloader=False)

def run_scraper():
    while True:
        main()
        time.sleep(86400)  # 每天運行一次

if __name__ == "__main__":
    # 啟動 Flask 應用和爬蟲
    threading.Thread(target=run_flask_app).start()  # 啟動 Flask 應用
    run_scraper()  # 啟動爬蟲

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), use_reloader=False)




