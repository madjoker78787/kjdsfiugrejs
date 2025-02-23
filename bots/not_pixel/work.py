import io
import random
from datetime import datetime, timedelta
from urllib.parse import urlparse, quote

from PIL import Image

import numpy as np

import time

from selenium.common import (TimeoutException,
                             ElementClickInterceptedException,
                             ElementNotInteractableException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver

from helper import logger


class PixelNotSeason:
    def __init__(self):
        self.driver = None

        self.link = "https://t.me/notpixel/app?startapp"
        self.list_coord = {}
        self.iframe = None

        self.re_enter = False

        self.info = None

        self.zoom_count = 2
        self.square_size = 19  # размер пикселя, прямопропрционально зуму: +х1 = -7px
        self.grid_step = 11  # количество клеток сетки 11х11

    def reload(self):
        self.driver.refresh()

    def hard_reload(self):
        self.driver.switch_to.default_content()
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-icon._BrowserHeaderButton_m63td_65"
                                                               "._BrowserHeaderTabIcon_m63td_111"))
            )
        except TimeoutException:
            return self.not_pixel_func(driver=self.driver, info=self.info)
        time.sleep(0.5)
        btn_icon = self.driver.find_elements(By.CLASS_NAME, "btn-icon._BrowserHeaderButton_m63td_65"
                                                            "._BrowserHeaderTabIcon_m63td_111")
        btn_icon[0].click()
        time.sleep(1)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-menu-item.rp-overflow"))
            )
        except TimeoutException:
            return self.not_pixel_func(driver=self.driver, info=self.info)
        btn_menu_item = self.driver.find_elements(By.CLASS_NAME, "btn-menu-item.rp-overflow")
        for x in btn_menu_item:
            if "Reload" in x.text:
                x.click()
        time.sleep(0.5)
        self.driver.switch_to.frame(self.iframe)

    def execute_js_code(self, x, y):
        js_code = """
        function simulatePointerEvents(element, startX, startY) {{
            const events = [
                new PointerEvent('pointerdown', {{ clientX: startX, clientY: startY, bubbles: true }}),
                new PointerEvent('pointermove', {{ clientX: startX, clientY: startY, bubbles: true }}),
                new PointerEvent('pointerup', {{ clientX: startX, clientY: startY, bubbles: true }})
            ];
            events.forEach(event => element.dispatchEvent(event));
        }}
        const canvas = document.querySelector('canvas');

        simulatePointerEvents(canvas, {0}, {1});
        """.format(x, y)
        self.driver.execute_script(js_code)

    def paint(self):

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_button_dvy5p_144"))
            )
            time.sleep(0.5)
        except TimeoutException:
            return self.not_pixel_func(driver=self.driver, info=self.info)
        time.sleep(3)
        zoom = self.driver.find_elements(By.CLASS_NAME, "_button_1txd3_27")
        for z in range(self.zoom_count):
            try:
                zoom[1].click()
                time.sleep(0.5)
            except ElementClickInterceptedException:
                self.click_intercepted()

        while True:
            break_point = False
            self.driver.switch_to.default_content()
            element_screenshot = self.iframe.screenshot_as_png
            image_data = io.BytesIO(element_screenshot)
            image = Image.open(image_data)
            width, height = image.size
            # Смещение для центра
            center_offset_x = 0
            center_offset_y = -3

            # Определяем пределы центральной области
            center_width, center_height = 209, 209
            left = (width - center_width) // 2 + center_offset_x
            upper = (height - center_height) // 2 + center_offset_y
            image_np = np.array(image)

            index = -1
            for i in range(0, center_height, self.square_size):
                for j in range(0, center_width, self.square_size):
                    index += 1
                    if index + 1 > len(self.list_coord) - 1:
                        self.driver.switch_to.default_content()
                        self.iframe = None
                        self.list_coord = {}
                        time.sleep(0.5)
                        return self.not_pixel_func(driver=self.driver, info=self.info)
                    try:
                        if self.list_coord[index]:

                            square_left = left + i
                            square_upper = upper + j
                            center_x = square_left + self.square_size // 2
                            center_y = square_upper + self.square_size // 2
                            center_pixel_color = image_np[center_y + 1, center_x + 1]
                            color = '#{:02x}{:02x}{:02x}'.format(center_pixel_color[0], center_pixel_color[1],
                                                                 center_pixel_color[2])

                            if color != self.list_coord[index] and color in colors:
                                self.driver.switch_to.frame(self.iframe)
                                self.change_color(new_hex=self.list_coord[index])
                                self.execute_js_code(x=center_x, y=center_y)
                                paint_btn = self.driver.find_element(By.CLASS_NAME, "_button_dvy5p_144")
                                if "Paint" in paint_btn.text:
                                    try:
                                        paint_btn.click()
                                        del self.list_coord[index]
                                        break_point = True
                                        break
                                    except ElementClickInterceptedException:
                                        self.click_intercepted()
                                    except ElementNotInteractableException:
                                        self.click_intercepted()
                                elif "No energy" in paint_btn.text:
                                    return True

                                if "No energy" in paint_btn.text:
                                    return True
                                self.driver.switch_to.default_content()
                    except:
                        pass

                if break_point:
                    break

    def change_color(self, new_hex):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_active_color_dvy5p_48"))
            )
        except TimeoutException:
            logger.error(f" | кнопки смены цвета не обнаружены")
            pass

        time.sleep(0.3)
        active_color = self.driver.find_element(By.CLASS_NAME, "_active_color_dvy5p_48")
        bg_color = active_color.value_of_css_property("background-color")
        rgba = bg_color.strip('rgba()')
        r, g, b, a = map(int, rgba.split(','))
        hex_color_active = "#{:02x}{:02x}{:02x}".format(r, g, b)
        if hex_color_active == new_hex:
            return
        else:
            try:
                active_color.click()
            except ElementClickInterceptedException:
                self.click_intercepted()

            change_colors = self.driver.find_elements(By.CLASS_NAME, "_color_item_epppt_22")
            for color in change_colors:
                bg = color.value_of_css_property("background-color")
                rgba_ = bg.strip('rgba()')
                r_, g_, b_, a_ = map(int, rgba_.split(','))
                hex_ = "#{:02x}{:02x}{:02x}".format(r_, g_, b_)

                if hex_ == new_hex:
                    try:
                        color.click()
                        time.sleep(0.3)
                        active_color.click()
                    except ElementClickInterceptedException:
                        pass

    def click_intercepted(self):
        divs = self.driver.find_elements(By.TAG_NAME, "div")
        for div in divs:
            try:
                div.click()
                print(div.get_attribute('class'))
                time.sleep(1)
            except:
                pass

    def get_list_coord(self):
        image_path = "bots/not_pixel/img/ready_image.png"
        img = Image.open(image_path)

        lst = {}

        target_color = (153, 21, 21)  # Цвет #991515 в RGB

        while True:
            center_x = random.randint(12, 1000)
            center_y = random.randint(12, 1000)
            index = 0
            for x in range(-5, 6):
                for y in range(-5, 6):
                    pixel_x, pixel_y = center_x + x, center_y + y
                    pixel_color = img.getpixel((pixel_x, pixel_y))
                    if pixel_color != target_color and "#{:02x}{:02x}{:02x}".format(*pixel_color) in colors:
                        lst[index] = "#{:02x}{:02x}{:02x}".format(*pixel_color)
                    index += 1
            if len(lst) > 10:
                break
        self.list_coord = lst
        self.link = f"https://t.me/notpixel/app?startapp=x{center_x}_y{center_y}"

    def not_pixel_func(self, driver: webdriver.Chrome, info=None, retry=0):
        self.driver = driver
        self.driver.switch_to.default_content()
        if info:
            self.info = info
        if retry > 10:
            return False
        self.get_list_coord()
        self.driver.set_window_size(950, 1000)
        self.reload()
        url = generate_telegram_url(self.link)
        self.driver.get(url)
        if info or self.info:
            self.info = info
            javascript_code = """
                            const element = document.createElement('div');
                            element.classList.add('session_info');
                            element.style.cssText = 'position: fixed; z-index: 2000; top: 10px; right: 10px;';
                            element.innerHTML = '{} - {}';
                            document.body.appendChild(element);
                            """.format(self.info['session_id'], self.info['session_name'])

            self.driver.execute_script(javascript_code)
            self.driver.implicitly_wait(5)

        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "popup-button.btn.primary.rp"))
            )
        except TimeoutException:
            return self.not_pixel_func(driver=self.driver, info=self.info, retry=retry + 1)

        time.sleep(0.3)
        launch_btn = self.driver.find_elements(By.CLASS_NAME, "popup-button.btn.primary.rp")
        for launch in launch_btn:
            if "launch" in launch.text.lower():
                launch.click()
                break

        try:
            WebDriverWait(self.driver, 25).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            # f = self.driver.find_element(By.TAG_NAME, "iframe")
            # src = f.get_attribute("src").split("7.10")
            # self.driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", f,
            #                            f"{src[0]}8.0{src[1]}")
        except TimeoutException:
            return self.not_pixel_func(driver=self.driver, info=self.info, retry=retry + 1)

        try:
            self.iframe = self.driver.find_element(By.TAG_NAME, "iframe")
            self.driver.switch_to.frame(self.iframe)

            start_time = datetime.now()
            while True:
                if datetime.now() - start_time > timedelta(seconds=40):
                    return self.not_pixel_func(driver=self.driver, retry=retry + 1)
                if self.driver.execute_script("return document.readyState") == "complete":
                    break
                else:
                    time.sleep(1)
            paint = self.paint()
            return paint
        except Exception as e:
            logger.error(f"{e}")
            return self.not_pixel_func(driver=self.driver, info=self.info, retry=retry + 1)


def generate_telegram_url(link):
    parsed_url = urlparse(link)

    domain = parsed_url.path.split("/")[1]
    appname = parsed_url.path.split("/")[2] if len(parsed_url.path.split("/")) > 2 else None

    op = f"tg://resolve?domain={domain}"

    if appname:
        op += f"&appname={appname}"

    query_params = parsed_url.query
    if query_params:
        op += f"&{query_params}"

    final_url = f"https://web.telegram.org/k/#?tgaddr={quote(op)}"

    return final_url


colors = [
    "#e46e6e",
    "#ffd635",
    "#7eed56",
    "#00ccc0",
    "#51e9f4",
    "#94b3ff",
    "#e4abff",
    "#ff99aa",
    "#ffb470",
    "#ffffff",
    "#be0039",
    "#ff9600",
    "#00cc78",
    "#009eaa",
    "#3690ea",
    "#6a5cff",
    "#b44ac0",
    "#ff3881",
    "#9c6926",
    "#898d90",
    "#6d001a",
    "#bf4300",
    "#00a368",
    "#00756f",
    "#2450a4",
    "#493ac1",
    "#811e9f",
    "#a00357",
    "#6d482f",
    "#000000"
]