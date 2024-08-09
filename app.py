import csv
from selenium import webdriver
import json
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from flask import Flask, render_template

UserInput = "https://www.ntsh.ntpc.edu.tw/p/403-1000-41-1.php?Lang=zh-tw"

driver = webdriver.Chrome('./chromedriver.exe')

# open the website
driver.get(UserInput)
driver.implicitly_wait(25)


app = Flask(__name__)

def scrape_ntsh():
    service = Service(executable_path=driver_path)
    options = Options()
    # 如果需要無頭模式（不顯示瀏覽器），可以添加以下選項
    # options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://www.ntsh.ntpc.edu.tw/')
        elements = driver.find_elements(By.CLASS_NAME, 'row.listBS')
        content = [element.text for element in elements]
    finally:
        driver.quit()
    
    return content

@app.route('/')
def index():
    content = scrape_ntsh()
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run(debug=True)
