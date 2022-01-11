from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
driver = webdriver.Firefox(executable_path=r'C:\Users\eeena\PycharmProjects\PPEInventoryWatchdog\geckodriver.exe')

driver.get('http://127.0.0.1:5000/')



def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath('/html/body/form/div[1]/input')
    except NoSuchElementException:
        return False
    return True
