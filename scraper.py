from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
def set_up_driver(chromedriver_path):
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(chromedriver_path,options=options)
    return driver

def main(chromedriver_path,url):
	driver = set_up_driver(chromedriver_path)
    driver.get(url)
    
if __name__ == "__main__":
	main("path/to/driver","link")
