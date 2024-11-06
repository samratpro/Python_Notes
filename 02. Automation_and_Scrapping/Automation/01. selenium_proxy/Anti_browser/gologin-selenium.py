import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from gologin import GoLogin
from selenium.webdriver.common.by import By
from time import sleep


gl = GoLogin({
	"token": "",
	"profile_id": "",
	# "extra_params":["--headless"]
	})


if platform == "linux" or platform == "linux2":
	chrome_driver_path = "./chromedriver"
elif platform == "darwin":
	chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
	chrome_driver_path = "chromedriver.exe"

debugger_address = gl.start()
service = Service(executable_path=chrome_driver_path)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("link")

sleep(1)
driver.quit()
gl.stop()
