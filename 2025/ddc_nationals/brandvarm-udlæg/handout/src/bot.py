import time
import traceback
import os
import uuid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

visiting = False

def review_expense(endpoint):
    global visiting

    if visiting:
        print("Already visiting an endpoint, please wait.")
        return False


    base_url = 'http://localhost:80'
    full_url = f"{base_url}{endpoint}"
    visiting = True

    browser = None 
    try:

        os.environ['HOME'] = '/tmp'

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--js-flags=--noexpose_wasm,--jitless')
        chrome_service = Service(port=9001)  # Force WebDriver port to 9001
        browser = webdriver.Chrome(service=chrome_service ,options=chrome_options)
        browser.get(full_url)
        time.sleep(10)
        return True

    except Exception as e:
        print(f"Error: {str(e)}", flush=True)
        traceback.print_exc()
        return False

    finally:
        if browser:
            try:
                browser.close()
                browser.quit()
            except:
                pass

        visiting = False
