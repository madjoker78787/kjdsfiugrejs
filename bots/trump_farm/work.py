import time

from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

def trump_farm_func(driver: webdriver.Chrome):
    # if dont work typography.service-work-text.css-dn7bit
    try:
        play = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-1dcsn2m"))
        )
        try:
            play.click()
        except ElementClickInterceptedException:
            close_button(driver=driver)
    except:
        pass

    energy = driver.find_element(By.CLASS_NAME, "css-1fzttwm")
    if int(energy.text) < 1:
        ...


def close_button(driver: webdriver.Chrome):
    try:
        close = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "css-hs5b5r"))
        )
        close.click()
        return True
    except TimeoutException:
        return False