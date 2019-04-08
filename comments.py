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

listOfevents = [
'ibWygf5WTkdGnP9yTy',
'qHF5CwSpxzMFf8cexS',
'APejpHKffEmyAdsttY'
]

for i in listOfevents:
	browser.get('http://127.0.0.1:8000/events/'+i)

	comment = browser.find_element_by_name('comment')
	comment.send_keys('comment1' + Keys.RETURN)
	time.sleep(5)
	submit = browser.find_element_by_name('submit')
	submit.click()
#browser.quit()
