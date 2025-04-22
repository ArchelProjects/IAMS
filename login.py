import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="C://browserdriver//geckodriver.exe")
driver = webdriver.Firefox(service=service)
driver.get("http://10.10.99.18:8002/login")

username = wait(driver,10).until(EC.presence_of_element_located((By.NAME, "username")))
password = driver.find_element(By.NAME, "password")
login_button = driver.find_element(By.ID, "login")

username.send_keys("chlmntl123@gmail.com")
password.send_keys("Dost2123")
login_button.click()
time.sleep(5)

actual_title = driver.title
expected_title = "Dashboard"

if expected_title not in actual_title:
    raise AssertionError("Login Test Failed")
print("IAMS Login Successfully!!!")
