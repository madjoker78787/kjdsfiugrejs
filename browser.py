import os

from selenium.webdriver.chrome.service import Service
from seleniumwire import webdriver
from seleniumwire.webdriver import ChromeOptions


def driver_browser(user_folder, port_, proxy_=None, dev=False) -> webdriver.Chrome:
    chrome_options = ChromeOptions()

    chrome_options.binary_location = "Application/chrome.exe"
    service = Service('driver/130/chromedriver.exe')

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("—disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"--remote-debugging-port={port_}")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--noerrordialogs")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--window-size=400, 800")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--deny-permission-prompts")

    if dev:
        chrome_options.add_argument("--enable-local-file-accesses")
        chrome_options.add_argument("--auto-open-devtools-for-tabs")

    chrome_options.add_argument(fr"--user-data-dir=.\Users\{user_folder}")

    if proxy_ is not None:
        proxy_options = {
            'proxy': {
                'http': f'{proxy_}',
                'https': f'{proxy_}',
                'no_proxy': 'localhost:127.0.0.1'
            }
        }
        driver_ = webdriver.Chrome(options=chrome_options, seleniumwire_options=proxy_options, service=service)
        return driver_
    else:
        driver_ = webdriver.Chrome(options=chrome_options, service=service)
        return driver_
