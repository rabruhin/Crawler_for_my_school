from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, render_template
import os

app = Flask(__name__)

def scrape_data():
    url = 'https://www.ntsh.ntpc.edu.tw/'
    
    # 打印工作目录，检查ChromeDriver路径
    print("Current Working Directory:", os.getcwd())
    chrome_driver_path = os.path.abspath('./bin/chromedriver')
    print("ChromeDriver Path:", chrome_driver_path)
    
    # 配置ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 以无头模式运行
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # 指定ChromeDriver的路径
    chrome_service = ChromeService(executable_path=chrome_driver_path)

    driver = webdriver.Chrome(service=chrome_service, options=options)
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


