from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template
from selenium.webdriver.chrome.service import Service
import os

app = Flask(__name__)
service= Service()

def scrape_data():
    url = 'https://www.ntsh.ntpc.edu.tw/'
    
    # 配置ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 初始化ChromeDriver
    driver = webdriver.Chrome(service=ChromeService(), options=options)
    driver.set_window_size(1024, 768)
    driver.get(url)

    try:
        # 等待元素加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'row listBS'))
        )

        elements = driver.find_elements(By.CLASS_NAME, 'row listBS')
        
        # 打印所有找到的元素数量和每个元素的HTML内容
        print(f"Found {len(elements)} elements with class 'row listBS'")
        for i, item in enumerate(elements):
            print(f"Element {i+1}: {item.get_attribute('innerHTML')}\n")

        scraped_data = []
        for item in elements:
            scraped_data.append(item.text.strip())
    
    finally:
        driver.quit()
    
    return scraped_data

@app.route('/')
def index():
    data = scrape_data()
    return render_template('index.html', data=data)

@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
