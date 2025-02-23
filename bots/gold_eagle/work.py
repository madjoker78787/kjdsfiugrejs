import time
import random
from datetime import timedelta, datetime

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver


def hard_reload(driver: webdriver.Chrome, retry=0):
    driver.switch_to.default_content()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-icon._BrowserHeaderButton_m63td_65"
                                                           "._BrowserHeaderTabIcon_m63td_111"))
        )
    except TimeoutException:
        return False
    time.sleep(0.5)
    btn_icon = driver.find_elements(By.CLASS_NAME, "btn-icon._BrowserHeaderButton_m63td_65"
                                                        "._BrowserHeaderTabIcon_m63td_111")
    btn_icon[0].click()
    time.sleep(1)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-menu-item.rp-overflow"))
        )
    except TimeoutException:
        return False
    time.sleep(0.3)
    btn_menu_item = driver.find_elements(By.CLASS_NAME, "btn-menu-item.rp-overflow")
    for x in btn_menu_item:
        if "reload" in x.text.lower():
            print(x.text.lower())
            x.click()

    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        src = iframe.get_attribute("src").split("7.10")
        driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", iframe,
                                   f"{src[0]}8.0{src[1]}")
        driver.switch_to.frame(iframe)

    except TimeoutException:
        if retry < 4:
            return hard_reload(driver=driver, retry=retry + 1)
        return False

    start_time = datetime.now()
    while True:
        if datetime.now() - start_time > timedelta(seconds=40):
            return hard_reload(driver=driver, retry=retry + 1)
        if driver.execute_script("return document.readyState") == "complete":
            break
        else:
            time.sleep(1)
    return True


def execute_js_code_pointer(driver: webdriver.Chrome, element, x, y):
    js_code = """
    function simulatePointerEvents(element, startX, startY) {{
        const events = [
            new PointerEvent('pointerdown', {{ clientX: startX, clientY: startY, bubbles: true }}),
            new PointerEvent('pointermove', {{ clientX: startX, clientY: startY, bubbles: true }}),
            new PointerEvent('pointerup', {{ clientX: startX, clientY: startY, bubbles: true }})
        ];
        events.forEach(event => element.dispatchEvent(event));
    }}
    const elem = document.querySelector('{0}');
    
    if (elem) {{
        simulatePointerEvents(elem, {1}, {2});
    }} else {{
        console.error("Element not found: {0}");
    }}

    """.format(element, x, y)
    driver.execute_script(js_code)


def execute_js_code_mouse(driver: webdriver.Chrome, element, x, y):
    js_code = """
    function simulatePointerEvents(element, startX, startY) {{
        const events = [
            new PointerEvent('mousedown', {{ clientX: startX, clientY: startY, bubbles: true }}),
            new PointerEvent('mousemove', {{ clientX: startX, clientY: startY, bubbles: true }}),
            new PointerEvent('mouseup', {{ clientX: startX, clientY: startY, bubbles: true }})
        ];
        events.forEach(event => element.dispatchEvent(event));
    }}
    const elem = document.querySelector('{0}');

    if (elem) {{
        simulatePointerEvents(elem, {1}, {2});
    }} else {{
        console.error("Element not found: {0}");
    }}

    """.format(element, x, y)
    driver.execute_script(js_code)


def gold_eagle_func(driver: webdriver.Chrome):
    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_label_15n79_25"))
        )
    except:
        return False

    while True:

        try:
            label = driver.find_element(By.CLASS_NAME, "_label_15n79_25")
            if int(label.text.split('/')[0]) > 50:
                try:
                    bad_request = driver.find_element(By.CLASS_NAME,
                                                      "Toastify__toast-container.Toastify__toast-container--top-center")
                    if "Bad request" in bad_request.text:
                        if not hard_reload(driver=driver):
                            return False
                except:
                    pass
                # driver.find_element(By.CLASS_NAME, "_tapArea_njdmz_15").click()
                execute_js_code_pointer(driver=driver, element="._tapArea_njdmz_15", x=0, y=0)
                time.sleep(random.uniform(0.001, 0.1))
            else:
                return True
        except Exception as e:
            print(e)
