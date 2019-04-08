from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
import time


browser = webdriver.Firefox()

browser.get('http://127.0.0.1:8000/login')
user = browser.find_element_by_name('username')
user.send_keys('pass')


password = browser.find_element_by_name('password')
password.send_keys('pass')

submit = browser.find_element_by_name('submit')
submit.click()

browser.get('http://127.0.0.1:8000/events/ibWygf5WTkdGnP9yTy')

button = browser.find_element_by_name('button1')
button.click()
time.sleep(5)
submit = browser.find_element_by_name('submit')
submit.click()
#browser.quit()

button = browser.find_element_by_name('button2')
button.click()
time.sleep(5)
submit = browser.find_element_by_name('submit')
submit.click()

button = browser.find_element_by_name('button3')
button.click()
time.sleep(5)
submit = browser.find_element_by_name('submit')
submit.click()