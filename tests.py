import os
import time
from datetime import datetime

import numpy as np
import os.path
from urllib.parse import urlparse, quote
from PIL import Image, ImageDraw
import io

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver



from browser import driver_browser


def test_main(user_, port_, pro=None):
    driver = driver_browser(user_folder=user_, port_=port_, proxy_=pro, dev=False)
    driver.set_window_size(800, 900)
    driver.get("https://web.telegram.org/k/")
    # driver.get("https://web.telegram.org/k/#?tgaddr=tg%3A//resolve%3Fdomain%3Dtverse%26startapp")
    # try:
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "popup-button.btn.primary.rp"))
    #     )
    # except:
    #     pass
    # launch_btn = driver.find_elements(By.CLASS_NAME, "popup-button.btn.primary.rp")
    # for launch in launch_btn:
    #     if "LAUNCH" in launch.text:
    #         launch.click()
    #         break
    while True:
        print(f"#1 - find 1 class\n"
              f"#2 - find many classes\n"
              f"#3 - click one class\n"
              f"#4 - click many classes\n"
              f"#5 - switch to frame\n"
              f"#6 - switch to default\n"
              f"#7 - if + in\n"
              f"#8 - my FUNC\n"
              f"#9 - click one css element\n"
              f"#10 - click many css elements\n"
              f"#11 - show driver requests")
        x = input("insert -> ")
        try:
            if x == "1":
                elem = input("enter name class -> ")
                e = driver.find_element(By.CLASS_NAME, elem)
                print("e = ", e)
                print(e.text)
                print("------------------------------------------")
            elif x == "2":
                elem = input("enter name class -> ")
                e = driver.find_elements(By.CLASS_NAME, elem)
                print("len ", len(e))
                for r, el in enumerate(e):
                    print(r, el.text)
                print("------------------------------------------")
            elif x == "3":
                elem = input("input class-> ")
                a = driver.find_element(By.CLASS_NAME, elem)
                a.click()
                print("click")
                print("------------------------------------------")
            elif x == "4":
                elem = input("input class and iter-> ")
                c = elem.split(' ')
                time.sleep(2)
                a = driver.find_elements(By.CLASS_NAME, c[0])
                a[int(c[1])].click()
                print("click")
                print("------------------------------------------")
            elif x == "5":
                iframe = driver.find_element(By.TAG_NAME, "iframe")
                print(iframe.get_attribute("src"))
                driver.switch_to.frame(iframe)
                print("switch")
                print("------------------------------------------")
            elif x == "6":
                driver.switch_to.default_content()
                print("switch")
                print("------------------------------------------")
            elif x == "7":
                elements = driver.find_elements(By.CLASS_NAME, "ui-link.blur")
                elements[4].click()
                time.sleep(15)
                elements[3].click()
                time.sleep(2)
                el = driver.find_element(By.CLASS_NAME, "d-flex.align-items-center")
                if "+" in el.text:
                    print("+ yes")
                else:
                    print("- no")
            elif x == "8":
                ...
                # javascript_code = """
                # const element = document.createElement('div');
                # element.classList.add('session_info');
                # element.style.cssText = 'position: fixed; z-index: 2000; top: 10px; right: 10px;';
                # element.innerHTML = '{} - {}';
                # document.body.appendChild(element);
                # """.format()
                #
                # driver.execute_script(javascript_code)
                #
                # driver.implicitly_wait(5)
                # draw_grid(driver)
                # get_colors(driver)
                # iframe = driver.find_element(By.TAG_NAME, "iframe")
                # driver.switch_to.frame(iframe)
                # zoom = driver.find_elements(By.CLASS_NAME, "_button_91s2c_27")
                # zoom[1].click()
                # time.sleep(0.5)
                # zoom[1].click()
                # driver.switch_to.default_content()
                # time.sleep(0.5)
                # square_size = 18
                #
                # element_screenshot = iframe.screenshot_as_png
                #
                # image_data = io.BytesIO(element_screenshot)
                # image = Image.open(image_data)
                #
                # width, height = image.size
                #
                # center_width, center_height = square_size * 11, square_size * 11
                # left = ((width - center_width) // 2) + 1
                # upper = ((height - center_height) // 2) - 2
                #
                # image_np = np.array(image)
                #
                # for i in range(0, center_width, square_size):
                #
                #     for j in range(0, center_height, square_size):
                #         square_left = left + i
                #         square_upper = upper + j
                #         center_x = square_left + square_size // 2
                #         center_y = square_upper + square_size // 2
                #
                #         center_pixel_color = image_np[center_y, center_x]
                #         color = '#{:02x}{:02x}{:02x}'.format(center_pixel_color[0], center_pixel_color[1],
                #                                              center_pixel_color[2])


            elif x == "9":
                el = input("enter tag element -> ")
            elif x == "10":
                el = input("enter tag element and iter (img, 105) -> ")
                els = el.split(', ')
                a = driver.find_elements(By.TAG_NAME, els[0])
                a[int(els[1])].click()

            elif x == "11":
                # req = driver.requests
                # for r in req:
                #     print(f"***************************\n{r}\n----------------------------")

                # Получение всех запросов
                # requests = driver.requests
                #
                # # Собираем URL изображений
                # image_urls = []
                #
                # # Фильтруем запросы, чтобы найти изображения
                # for request in requests:
                #     if request.response and 'image' in request.response.headers.get('Content-Type', ''):
                #         image_urls.append(request.url)
                #
                # # Выводим найденные URL изображений
                # print("Найденные изображения:")
                # for url in image_urls:
                #     print(url)

                requests = driver.requests

                # Отфильтровываем запросы на основе типа
                blob_urls = []

                for request in requests:
                    if request.response and 'blob:' in request.url:
                        blob_urls.append(request.url)

                # Выводим все найденные Blob URL
                print("Найденные Blob URL:")
                for url in blob_urls:
                    print(url)

        except Exception as e:
            print(e)


def execute_js_code(driver: webdriver.Chrome, x, y):
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
    driver.execute_script(js_code)


def draw_grid(driver: webdriver.Chrome):
    # c_x = int(input("смещение по x -> "))
    # c_y = int(input("смещение по y -> "))
    # size_ = int(input("размер квадрата -> "))
    # predel = int(input("пределы -> "))
    try:
        frame = driver.find_element(By.TAG_NAME, 'iframe')

        driver.switch_to.frame(frame)
        zoom = driver.find_elements(By.CLASS_NAME, "_button_1txd3_27")
        zoom[1].click()
        time.sleep(0.5)
        zoom[1].click()
        time.sleep(1)

        driver.switch_to.default_content()

        # Находим элемент по селектору (например, ID или классу)
        # frame = driver.find_element(By.TAG_NAME, 'iframe')  # Замените на ваш селектор

        # Делаем скриншот элемента
        element_screenshot = frame.screenshot_as_png

        # Декодируем скриншот в изображении
        image_data = io.BytesIO(element_screenshot)
        image = Image.open(image_data)

        # Определяем размер изображения
        width, height = image.size

        # Смещение для центра
        center_offset_x = 0
        center_offset_y = -3

        # Определяем пределы центральной области 78x78
        center_width, center_height = 209, 209
        left = (width - center_width) // 2 + center_offset_x
        upper = (height - center_height) // 2 + center_offset_y

        # Инициализация рисования сетки
        draw = ImageDraw.Draw(image)

        # Размер квадрата
        square_size = 19
        # square_size = size_
        found_pixels = []  # Список для хранения информации о пикселях
        v = 0
        # Проходим по каждому 13x13 квадрату в центральной области
        for i in range(0, center_width, square_size):
            for j in range(0, center_height, square_size):
                print("v", v)
                v += 1
                # Координаты квадрата
                square_left = left + i
                square_upper = upper + j
                square_right = square_left + square_size
                square_lower = square_upper + square_size

                # Рисуем квадрат сетки
                draw.rectangle([square_left, square_upper, square_right, square_lower], outline="red", width=1)

                # Находим цвет центрального пикселя квадрата
                center_x = square_left + square_size // 2
                center_y = square_upper + square_size // 2

                # Проверяем, чтобы координаты находились в пределах изображения
                if 0 <= center_x < width and 0 <= center_y < height:
                    center_pixel_color = image.getpixel((center_x, center_y))

                    # Преобразуем цвет в формате RGB
                    found_pixels.append({
                        "coordinates": (center_x, center_y),
                        "color": center_pixel_color
                    })

                    # # Помечаем центральный пиксель белым цветом
                    # draw.point((center_x, center_y), fill=(255, 255, 255))  # Устанавливаем белый цвет для центрального пикселя

        # Сохраняем изображение с сеткой
        image.save(f"test_pixel/imgs/1.png")
        image.show()
        # Выводим цвета и координаты центральных пикселей
        # print("Центральные пиксели квадратов (координаты и цвет):")
        # for pixel in found_pixels:
        #     print(f"Координаты: {pixel['coordinates']}, Цвет: {pixel['color']}")

    except Exception as e:
        print(e)


def get_colors(driver: webdriver.Chrome):
    frame = driver.find_element(By.TAG_NAME, 'iframe')

    driver.switch_to.frame(frame)
    zoom = driver.find_elements(By.CLASS_NAME, "_button_1txd3_27")
    zoom[1].click()
    time.sleep(0.5)
    zoom[1].click()
    time.sleep(1)

    driver.switch_to.default_content()

    element_screenshot = frame.screenshot_as_png
    image_data = io.BytesIO(element_screenshot)
    image = Image.open(image_data)
    width, height = image.size

    # Смещение для центра
    center_offset_x = 0
    center_offset_y = -3
    square_size = 19

    # Определяем пределы центральной области
    center_width, center_height = 209, 209
    left = (width - center_width) // 2 + center_offset_x
    upper = (height - center_height) // 2 + center_offset_y
    image_np = np.array(image)

    index = 0
    for i in range(0, center_height, square_size):
        for j in range(0, center_width, square_size):
    # for i in range(0, center_width, square_size):
    #     for j in range(0, center_height, square_size):
            square_left = left + i
            square_upper = upper + j
            center_x = square_left + square_size // 2
            center_y = square_upper + square_size // 2
            center_pixel_color = image_np[center_y + 1, center_x + 1]
            color = '#{:02x}{:02x}{:02x}'.format(center_pixel_color[0], center_pixel_color[1],
                                                 center_pixel_color[2])
            print(index, f':\"{color}\",')
            index += 1
