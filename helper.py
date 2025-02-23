import json
import os
import sys
import time
import zlib
from datetime import datetime, timedelta
from urllib.parse import urlparse, quote
import subprocess

import requests
from loguru import logger

import psycopg2
from psycopg2 import sql


from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException


from config import settings
from settings_bots import lst_bots


logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
                                   " | <level>{level: <8}</level>"
                                   " | <cyan><b>{line}</b></cyan>"
                                   " - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)


def replace_override(lst: list[str], file_name, text):
    text_from_replace = text.split(', ')
    updated_content = [line.replace(text_from_replace[0], text_from_replace[1]) for line in lst]
    with open(file_name, 'w', encoding='utf-8') as file:
        file.writelines(updated_content)


def remove_override(lst: list[str], file_name, text):
    x = 0
    output_lines = []
    content = text.split('\n')
    while x < len(lst):
        if lst[x].strip() in content:
            x += len(content)
        else:
            output_lines.append(lst[x])
            x += 1
    with open(file_name, 'w', encoding='utf-8') as outfile:
        outfile.writelines(output_lines)


def local_override(driver: webdriver.Chrome, text, file_url, type_, location):
    logger.warning(f"запуск local override")
    url = ""
    if location == "html":
        scr = driver.find_elements(By.TAG_NAME, "script")
        for x in scr:
            if file_url in x.get_attribute("src") and ".js" in x.get_attribute("src"):
                url = x.get_attribute("src")
                break
    elif location == "request":
        for req in driver.requests:
            if file_url in req.url and ".js" in req.url:
                url = req.url
    # for req in driver.requests:
    #     if file_url in req.url and ".js" in req.url:
    response = requests.get(url)
    if response.status_code == 200:
        replacer = '/'
        file_out_put = url.replace('https://', '').split(replacer)

        base_path = f"OVERRIDE/{replacer.join(file_out_put[:-1])}"
        if not os.path.basename(base_path) == file_out_put[-1]:
            logger.warning(f"загружаю новый файл {file_out_put[-1]}")
            try:
                with open(f"{base_path}/{file_out_put[-1]}", 'wb') as f:
                    f.write(response.content)
            except:
                pass
            try:
                with open(f"{base_path}/{file_out_put[-1]}", 'r', encoding='utf-8') as file:
                    content = file.readlines()
                    if type_ == "remove":
                        remove_override(lst=content, file_name=f"{base_path}/{file_out_put[-1]}", text=text)
                    if type_ == "replace":
                        replace_override(lst=content, file_name=f"{base_path}/{file_out_put[-1]}", text=text)
            except:
                pass
        return True


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


def decode_string(s: bytes):
    decompressed = zlib.decompress(s, zlib.MAX_WBITS | 16)
    d_string = decompressed.decode('utf-8')
    decode_json = json.loads(d_string)
    return decode_json


def get_proxy():
    list_proxy = []
    with open('proxy.txt', 'r') as file:
        for item in file:
            list_proxy.append(item)
    return list_proxy


def init_postgres():
    conn = psycopg2.connect(
        dbname="postgres",
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [settings.DB_NAME])
    exists = cursor.fetchone() is not None
    if not exists:
        logger.info("создаем базу данных Telegram")
        query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier("Telegram"))
        cursor.execute(query)
        logger.info("база данных Telegram успешно создана")
        cursor.close()
        conn.close()
    else:
        logger.info("база данных Telegram уже создана")

    if not check_table_exist(table_name=settings.TABLE_TELEGRAM):
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        logger.info(f"создаем таблицу {settings.TABLE_TELEGRAM}")
        query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    number VARCHAR(100),
                    port VARCHAR(100),
                    seed VARCHAR(300),
                    work VARCHAR(100) DEFAULT 1
                )
                """).format(sql.Identifier(settings.TABLE_TELEGRAM))
        cursor.execute(query)
        conn.commit()
        cursor.execute("INSERT INTO data(number, port, work) VALUES(%s, %s, %s)", ("test", "8742", "0"))
        conn.commit()
        cursor.close()
        conn.close()
        logger.success("таблица data создана")
    else:
        logger.info("таблица data уже создана")

    for _, table_name in lst_bots.items():
        create_table(table_name=table_name['table_name'])


def check_table_exist(table_name):
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    query = """
    SELECT EXISTS (
        SELECT 1 
        FROM information_schema.tables 
        WHERE table_name = %s
    );
    """
    cursor.execute(query, (table_name,))
    table_exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if table_exists:
        return True
    else:
        return False


def create_table(table_name):
    if not check_table_exist(table_name):
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        conn.autocommit = True
        logger.info(f"создаем таблицу {settings.DB_NAME}.{table_name}")
        query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    data_id VARCHAR(100),
                    last_visit VARCHAR(100)
                )
                """).format(sql.Identifier(table_name))
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        logger.success(f"таблица {table_name} создана")


def get_active_accounts():
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, number, port FROM data WHERE work = %s ORDER BY id ASC", ("1", ))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_last_visit(id_, table_name):
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    query = sql.SQL("SELECT last_visit FROM {} WHERE data_id = %s").format(sql.Identifier(table_name))
    cursor.execute(query, (str(id_),))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result if result is not None else ["01.01.1970 00:00"]


def update_time(id_, table_name):
    try:
        conn = psycopg2.connect(
            dbname=settings.DB_NAME,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        query_ = sql.SQL("SELECT data_id FROM {} WHERE data_id = %s").format(sql.Identifier(table_name))
        cursor.execute(query_, (str(id_),))
        get_data_ = cursor.fetchone()
        if not get_data_:
            query = sql.SQL("INSERT INTO {}(data_id, last_visit) VALUES(%s, %s)").format(sql.Identifier(table_name))
            cursor.execute(query, (str(id_), datetime.now().strftime("%d.%m.%Y %H:%M"),))
        else:
            query = sql.SQL("UPDATE {} SET last_visit = %s WHERE data_id = %s").format(sql.Identifier(table_name))
            cursor.execute(query, (datetime.now().strftime("%d.%m.%Y %H:%M"), str(id_),))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"{id_} | {table_name} | {e}")


# def hard_reload(driver: webdriver.Chrome, retry=0):
#     driver.switch_to.default_content()
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "btn-icon._BrowserHeaderButton_m63td_65"
#                                                            "._BrowserHeaderTabIcon_m63td_111"))
#         )
#     except TimeoutException:
#         return False
#     time.sleep(0.5)
#     btn_icon = driver.find_elements(By.CLASS_NAME, "btn-icon._BrowserHeaderButton_m63td_65"
#                                                         "._BrowserHeaderTabIcon_m63td_111")
#     btn_icon[0].click()
#     time.sleep(1)
#
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CLASS_NAME, "btn-menu-item.rp-overflow"))
#         )
#     except TimeoutException:
#         return False
#     btn_menu_item = driver.find_elements(By.CLASS_NAME, "btn-menu-item.rp-overflow")
#     for x in btn_menu_item:
#         if "Reload" in x.text:
#             x.click()
#
#     try:
#         WebDriverWait(driver, 25).until(
#             EC.presence_of_element_located((By.TAG_NAME, "iframe"))
#         )
#         iframe = driver.find_element(By.TAG_NAME, "iframe")
#         src = iframe.get_attribute("src").split("7.10")
#         driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", iframe,
#                                    f"{src[0]}8.0{src[1]}")
#         driver.switch_to.frame(iframe)
#
#     except TimeoutException:
#         if retry < 4:
#             return hard_reload(driver=driver, retry=retry + 1)
#         return False
#
#     start_time = datetime.now()
#     while True:
#         if datetime.now() - start_time > timedelta(seconds=40):
#             return hard_reload(driver=driver, retry=retry + 1)
#         if driver.execute_script("return document.readyState") == "complete":
#             break
#         else:
#             time.sleep(1)
#     return True


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
    const canvas = document.querySelector({0});

    simulatePointerEvents(canvas, {1}, {2});
    """.format(element, x, y)
    driver.execute_script(js_code)