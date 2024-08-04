from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# 設置 ChromeDriver 的路徑
driver_path = 'C:\\Users\\user\\PycharmProjects\\ntshcrawler\\chromedriver.exe'

# 創建 ChromeDriver 的 Service 對象
service = Service(executable_path=driver_path)

# 創建 ChromeOptions 對象（可選）
options = Options()

# 如果需要無頭模式（不顯示瀏覽器），可以添加以下選項
# options.add_argument('--headless')

# 創建 WebDriver 實例
driver = webdriver.Chrome(service=service, options=options)

try:
    # 打開目標網站
    driver.get('https://www.ntsh.ntpc.edu.tw/')

    # 查找所有 class 為 "row listBS" 的元素
    elements = driver.find_elements(By.CLASS_NAME, 'row.listBS')

    # 提取並打印這些元素的文本內容
    for element in elements:
        print(element.text)

finally:
    # 關閉瀏覽器
    driver.quit()
