from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys


browser = webdriver.Firefox()
browser.get('http://127.0.0.1:8000/signup')
elem = browser.find_element_by_name('username')
elem.send_keys('pass4')

email = browser.find_element_by_name('email')
email.send_keys('pass4')
password1 = browser.find_element_by_name('password')
password1.send_keys('pass4')


print("Found")


submit = browser.find_element_by_name('submit')

submit.send_keys(Keys.RETURN)

assert 'OneLyf' in browser.title
browser.quit()