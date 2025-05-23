# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D42BF45DD6F0C6403A2869BD95AA90FAC790B9D76835719593AA7F55720D0FDF51D1FD905B1BEF114B578A7E6ABFAF5BD8ED2D1C703125689219EBA80318076D272C14A8E099D4499830F1E61E25D4207E97B27ED3C289631C9FE4D512FBFF5DE08E13995AEEF747AB7810E089FFD615955C229036FF6964A742015EF4EF572AA468033C5141F03C7418141EAD2BC1E35F67B8B86FF2F02DAD020E1771F9773EE005A8CC89EF00A2175D44B9FBA6393C5AE7D29460142EFFCF2B24AE7080A6563359F7EFE91DADF1D799BC196D9EB0567A46667E6534F17C404834421BB1B56563068C4CAA64FA66B2659AA1BA594C71576D97889B78702C5C40EA5DD10552332DAD9BFDBCB0569C0B2FFFDACF7383B13CD43383895B8C75EABD717F35FBE9380C8D82047E4E4E7FE75F0597DF444E62E746AE3C8CC31ADC0EC6294933F5E75EE6830E2AD38A69217B2F7B4228AF88116054FD5C4AB373FB3C002E0832995B89
                        "})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
