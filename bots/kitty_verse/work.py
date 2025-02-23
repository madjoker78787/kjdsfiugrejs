import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver


def kitty_verse_func(driver: webdriver.Chrome):
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, "preloader-status.preloader-status-blinker"))
        )
    except TimeoutException:
        ...
    preloader = driver.find_element(By.CLASS_NAME, "preloader-status.preloader-status-blinker")
    if "кликни" in preloader.text.lower():
        spans = driver.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if "кликни" in span.text.lower():
                span.click()
                break

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "popup-bonus-button"))
        )
    except TimeoutException:
        pass
    bonus = driver.find_element(By.CLASS_NAME, "popup-bonus-button")
    if bonus:
        bonus.click()

    try:
        mcv = driver.find_element(By.CLASS_NAME, "monster-counter-value")
        mcv_2 = int(mcv.text.split('/')[0])
    except NoSuchElementException:
        pass

    try:
        mrb = driver.find_element(By.CLASS_NAME, "monster-counter-retry-button")
    except NoSuchElementException:
        pass
    # monster-counter-exit-button
    # hp-value сплитнуть пробелом и ноль получить
    # monster-counter-value
    # close-button
    print("имитация работы kitty")
    time.sleep(30)
    return True