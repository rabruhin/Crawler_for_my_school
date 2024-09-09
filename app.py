from flask import Flask, render_template_string
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)

def crawl_main_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 使用無頭模式
    chrome_options.add_argument("--no-sandbox")  # Render 環境中需要添加此參數
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免共享內存問題
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # 剩餘代碼保持不變


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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
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

def generate_html():
    # Output is handled by Flask, so no need to write to output.html
    pass

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
    app.run(debug=True, use_reloader=False)

def run_scraper():
    while True:
        main()
        time.sleep(86400)  # 每天运行一次

if __name__ == "__main__":
    # Start Flask server in a separate thread
    threading.Thread(target=run_flask_app).start()
    # Start the scraper in the main thread
    run_scraper()

