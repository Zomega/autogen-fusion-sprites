

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time


driver_delay = 5
fakemon_url = "https://japeal.com/fmm/"




def get_driver():
    options = Options()
    options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
    return webdriver.Firefox(executable_path=r'C:/Selenium/geckodriver.exe', options=options)


def get_element_by_id(driver:WebDriver, id_element:str) -> WebElement:
    element = None
    locator = (By.ID, id_element)
    try:
        element = WebDriverWait(driver, driver_delay).until(EC.presence_of_element_located(locator))
    except TimeoutException:
        print(f"[get_element_by_id] Failed to get {id_element}")
    return element

def get_element_by_xpath(driver:WebDriver, xpath_element:str) -> WebElement:
    element = None
    locator = (By.XPATH, xpath_element)
    try:
        element = WebDriverWait(driver, driver_delay).until(EC.presence_of_element_located(locator))
    except TimeoutException:
        print(f"[get_element_by_id] Failed to get {xpath_element}")
    return element

def get_element_by_class(driver:WebDriver, class_element:str, is_loud=True) -> WebElement:
    element = None
    locator = (By.CLASS_NAME, class_element)
    try:
        element = WebDriverWait(driver, driver_delay).until(EC.presence_of_element_located(locator))
    except TimeoutException:
        if is_loud:
            print(f"[find_element_by_class] Failed to get {class_element}")
    return element


# sometimes appear, sometimes doesn't
def accept_all_cookies(driver:WebDriver):
    class_accept = "cc-accept-all"
    try:
        element_accept = get_element_by_class(driver, class_accept, is_loud=False)
        element_accept.click()
    except:
        pass
        # print("no cookies to accept")
    else:
        # print("accepting all cookies")
        time.sleep(1)

def clear_background(driver:WebDriver):
    xpath_background = "/html/body/div[1]/div/div[5]/div[4]/div/div/main/div[4]/style[2]"
    script = ""
    script += "function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};"
    script += f"getElementByXpath('{xpath_background}').innerHTML='';"
    driver.execute_script(script)   

def clear_element(element:WebElement):
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)

def adapt_zoom(driver:WebDriver):
    # Creates non-blurry sprites with 3x3 pixels
    driver.execute_script('document.body.style.MozTransform = "scale(0.80)";')
    driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')


id_pokemon_selector = "Limagediv2"
id_textbox = "msdropdown20_titleText"
id_body = "pbox_body"
id_color = "pbox_color"
id_head = "pbox_head"
id_hand = "pbox_LH"
id_fakemon_right_hand = "bbox_RH"
id_fakemon_left_hand  = "bbox_LH"
id_size = "numberSize"
id_position_x = "numberX"
class_selected = "selected"






def create_driver():
    driver = get_driver()
    print(" ")
    driver.set_window_position(60, 1)
    driver.set_window_size(744, 866)
    driver.get(fakemon_url)
    return driver


def init_website(driver:WebDriver):
    # print("waiting for the default portrait to load")
    time.sleep(5)
    adapt_zoom(driver)
    accept_all_cookies(driver)
    clear_background(driver)


def handle_body(driver:WebDriver, body:str):
    # print("clicking on pokemon portrait")
    element_pokemon_selector = get_element_by_id(driver, id_pokemon_selector)
    element_pokemon_selector.click()
    time.sleep(1)

    # print("writing pokemon name (body)")
    element_textbox = get_element_by_id(driver, id_textbox)
    clear_element(element_textbox)
    element_textbox.send_keys(body)
    time.sleep(1)

    # print("selecting the best choice")
    element_selected = get_element_by_class(driver, class_selected)
    element_selected.click()
    time.sleep(1)

    # print("clicking on body")
    element_selected = get_element_by_id(driver, id_body)
    element_selected.click()
    time.sleep(1)


def handle_head(driver:WebDriver, head:str):
    # print("clicking on pokemon portrait")
    element_pokemon_selector = get_element_by_id(driver, id_pokemon_selector)
    element_pokemon_selector.click()
    time.sleep(1)

    # print("writing pokemon name (head)")
    element_textbox = get_element_by_id(driver, id_textbox)
    clear_element(element_textbox)
    element_textbox.send_keys(head)
    time.sleep(1)

    # print("selecting the best choice")
    element_selected = get_element_by_class(driver, class_selected)
    element_selected.click()
    time.sleep(1)

    # print("clicking on color")
    element_selected = get_element_by_id(driver, id_color)
    element_selected.click()
    time.sleep(1)

    # print("clicking on head")
    element_selected = get_element_by_id(driver, id_head)
    element_selected.click()
    time.sleep(1)

    # print("clicking on hands")
    element_selected = get_element_by_id(driver, id_hand)
    element_selected.click()
    time.sleep(1)


def fix_rotom_cancer():
    # print("clicking on right hand")
    element_fakemon_right_hand = get_element_by_id(driver, id_fakemon_right_hand)
    element_fakemon_right_hand.click()
    time.sleep(1)

    # print("changing the size of the arm")
    element_size = get_element_by_id(driver, id_size)
    clear_element(element_size)
    element_size.send_keys("-22")
    time.sleep(1)

    # print("changing the position of the arm")
    element_position_x = get_element_by_id(driver, id_position_x)
    clear_element(element_position_x)
    element_position_x.send_keys("20")
    time.sleep(1)

    # print("clicking on left hand")
    element_fakemon_left_hand = get_element_by_id(driver, id_fakemon_left_hand)
    element_fakemon_left_hand.click()
    time.sleep(1)

    # print("changing the position of the arm")
    element_position_x = get_element_by_id(driver, id_position_x)
    clear_element(element_position_x)
    element_position_x.send_keys("-20")
    time.sleep(1)


def create_fusion(driver:WebDriver, head:str, body:str):
    handle_body(driver, body)
    handle_head(driver, head)
    fix_rotom_cancer()


head_list = []
head_list.append("Electabuzz")
head_list.append("Magmar")
head_list.append("Mewtwo")
head_list.append("Typhlosion")
head_list.append("Ledyba")
head_list.append("Ledian")
head_list.append("Ariados")
head_list.append("Lanturn")
head_list.append("Ampharos")
head_list.append("Azumarill")
head_list.append("Sudowoodo")
head_list.append("Politoed")


body = "Rotom"


driver = create_driver()
print("START")
init_website(driver)

for head in head_list:
    filename = f"{head}-{body}.png"
    create_fusion(driver, head, body)
    print(filename, driver.save_screenshot(f"new_rotom/{filename}"))

driver.close()
print("END")