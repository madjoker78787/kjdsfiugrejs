import time

import psycopg2

from dump_db.dump_db import dump_data_db
from browser import driver_browser

from config import settings


def start_one():
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, number FROM data ORDER BY id")
    nums = cursor.fetchall()
    for i in nums:
        print(f"id [ {i[0]} ] номер [ {i[1]} ]")

    id_ = int(input("выбери номер(не id) -> "))
    cursor.execute("SELECT id, number, port FROM data WHERE id = %s", (id_,))
    num = cursor.fetchone()
    driver = driver_browser(user_folder=num[1],
                            port_=num[2],
                            proxy_=settings.PROXY
                            )
    cursor.close()
    conn.close()
    driver.set_window_size(950, 1000)
    driver.get("https://web.telegram.org/k/")

    try:
        time.sleep(999999999)
    except KeyboardInterrupt:
        print("остановлен")


def add_account():
    number = input("номер телефона -> ")
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT number, port FROM data")
    numbers = cursor.fetchall()
    for i in numbers:
        if number.replace('-', '') == str(i[0]).replace('-', ''):
            res = input(f"Номер {str(i[0]).replace('-', '')} уже есть, обновить? [ y/n ] ")
            if res.lower() == "y":
                print("Обновление...")
                driver = driver_browser(
                    user_folder=number,
                    port_=8742,
                    proxy_=settings.PROXY,
                    dev=False
                )
                driver.get("https://web.telegram.org/k/")
                time.sleep(999999999)

    not_exist = input("Номера нет, продолжить? [Y/N] ")
    if not_exist.lower() == "n":
        return
    print("Продолжаем...")
    cursor.execute("SELECT port FROM data ORDER BY id DESC LIMIT 1")
    port = cursor.fetchone()
    cursor.execute("INSERT INTO data(number, port) VALUES(%s, %s)",
                   (number, int(port[0]) + 1,))
    conn.commit()
    cursor.close()
    conn.close()

    dump_data_db()

    driver = driver_browser(
        user_folder=number,
        port_=int(port[0]) + 1,
        proxy_=settings.PROXY,
        dev=False
    )

    driver.get("https://web.telegram.org/k/")
    try:
        time.sleep(999999999)
    except KeyboardInterrupt:
        print("остановлен")


def get_five_accounts():
    a_ = int(input("введи id -> "))
    conn = psycopg2.connect(
        dbname=settings.DB_NAME,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, number, port FROM data WHERE id >= %s ORDER BY id ASC LIMIT 5", (a_,))
    accs = cursor.fetchall()
    print(f"последний id {accs[-1][0]}")
    return accs


def pool_many(accs):
    driver = driver_browser(user_folder=accs[1],
                            port_=accs[2],
                            proxy_="http://dfxhfhaw-rotate:rdhoxlgxoqub@p.webshare.io:80/")
    driver.set_window_size(950, 1000)

    driver.get("https://web.telegram.org/k")
    time.sleep(2)
    javascript_code = """
                    const element = document.createElement('div');
                    element.classList.add('session_info');
                    element.style.cssText = 'position: fixed; z-index: 2000; top: 10px; right: 10px;';
                    element.innerHTML = '{} - {}';
                    document.body.appendChild(element);
                    """.format(accs[0], accs[1])

    driver.execute_script(javascript_code)

    driver.implicitly_wait(5)

    # try:
    #     WebDriverWait(driver, 40).until(
    #         EC.presence_of_element_located((By.CLASS_NAME, "popup-button.btn.primary.rp"))
    #     )
    # except:
    #     pass
    # launch_btn = driver.find_elements(By.CLASS_NAME, "popup-button.btn.primary.rp")
    #
    # for launch in launch_btn:
    #     try:
    #         if "LAUNCH" in launch.text or "запустить" in launch.text:
    #             launch.click()
    #             time.sleep(2)
    #     except:
    #         pass

    # try:
    #     WebDriverWait(driver, 40).until(
    #         EC.presence_of_element_located((By.TAG_NAME, "iframe"))
    #     )
    #     f = driver.find_element(By.TAG_NAME, "iframe")
    #     src = f.get_attribute("src").split("7.10")
    #     driver.execute_script("arguments[0].setAttribute('src', arguments[1]);", f, f"{src[0]}8.0{src[1]}")
    # except:
    #     print(f"{lst[1]} dont connect")
    try:
        time.sleep(999999)
    except KeyboardInterrupt:
        pass
