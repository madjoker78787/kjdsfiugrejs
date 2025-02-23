import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver


def tiny_verse_func(driver: webdriver.Chrome):
    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ui-link.blur"))
        )
    except:
        pass

    elements = driver.find_elements(By.CLASS_NAME, "ui-link.blur")
    for i in elements:
        print(i.text)
    print("имитация работы")
    time.sleep(10)
    # elements[4].click()
    # time.sleep(15)
    # elements[3].click()
    # time.sleep(2)
    # el = driver.find_element(By.CLASS_NAME, "d-flex.align-items-center")
    # if "+" not in el.text:
    #     driver.find_element(By.CLASS_NAME, "ui-button").click()
    #     time.sleep(5)
    return True