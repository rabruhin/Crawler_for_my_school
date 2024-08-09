from flask import Flask, send_file
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def crawl_site():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        url = "https://www.ntsh.ntpc.edu.tw/p/403-1000-41-1.php?Lang=zh-tw"
        driver.get(url)
        time.sleep(3)
        elements = driver.find_elements(By.CSS_SELECTOR, ".row.listBS")

        # 保存爬取的數據到 output.txt
        with open("output.txt", "w", encoding="utf-8") as file:
            for element in elements:
                file.write(element.text + "\n")

        # 將 output.txt 轉換為 HTML 文件
        convert_txt_to_html("output.txt", "output.html")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()

def convert_txt_to_html(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as txt_file:
        lines = txt_file.readlines()

    html_content = "<html>\n<head>\n<title>Output</title>\n</head>\n<body>\n"
    html_content += "<h1>爬取的數據</h1>\n<ul>\n"
    
    for line in lines:
        html_content += f"<li>{line.strip()}</li>\n"
    
    html_content += "</ul>\n</body>\n</html>"

    with open(output_file, "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

# 設置 Flask 路由來返回 HTML 文件
@app.route('/')
def serve_html():
    return send_file('output.html')

# 每小時運行一次爬蟲
if __name__ == '__main__':
    while True:
        crawl_site()
        time.sleep(3600)
