
from selenium import webdriver
import time


driver = webdriver.Firefox(executable_path=r'C:\Users\eeena\PycharmProjects\PPEInventoryWatchdog\geckodriver.exe')


driver.get('http://127.0.0.1:5000/')


time.sleep(4)


driver.find_element_by_xpath('/html/body/form/div[1]/input').click()

time.sleep(4)

driver.close()
