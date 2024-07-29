import base64
import logging
import time

import folium
from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.chrome.options import Options as ChromeOptions


options = ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-extensions")
LOGGER.setLevel(logging.WARNING)


def map_image(map: folium.Map) -> bytes:
    '''Запускает html полученный из folium map с уже наложенным
    маршрутом для получения байтов скриншота маршрута'''

    driver = webdriver.Remote('http://selenium:4444/wd/hub', options=options)

    html = map.get_root().render()

    html_bs64 = base64.b64encode(html.encode('utf-8')).decode()  #  type: ignore
    driver.get("data:text/html;base64," + html_bs64)

    time.sleep(3)

    img_bytes = driver.get_screenshot_as_png()
    driver.quit()

    return img_bytes
