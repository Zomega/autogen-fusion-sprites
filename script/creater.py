

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

basic_delay = 1
is_loud = True
have_cookies = None
xpath_with_cookies    = "/html/body/div[3]/div/div[5]/div[4]/div/div/main/div[4]/style[2]" 
xpath_without_cookies = "/html/body/div[1]/div/div[5]/div[4]/div/div/main/div[4]/style[2]"


def log(message:str):
    if is_loud:
        print(message)


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
    global have_cookies
    class_accept = "cc-accept-all"
    try:
        element_accept = get_element_by_class(driver, class_accept, is_loud=False)
        element_accept.click()
    except:
        have_cookies = False
        log("no cookies to accept")
    else:
        have_cookies = True
        log("accepting all cookies")
        time.sleep(basic_delay)

def clear_background(driver:WebDriver):
    xpath = xpath_with_cookies if have_cookies else xpath_without_cookies

    script = ""
    script += f"var xpath = '{xpath}';"
    script += "function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};"
    script += "var element = getElementByXpath(xpath);"
    script += "element.innerHTML='';"

    try:
        driver.execute_script(script)
    except Exception as e:
        print(script)
        # driver.close()
        exit()

def clear_element(element:WebElement):
    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.DELETE)

def adapt_zoom(driver:WebDriver):
    # Creates non-blurry sprites with 3x3 pixels
    log("zooming at 80%")
    driver.execute_script('document.body.style.MozTransform = "scale(0.80)";')
    driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')


id_pokemon_selector = "Limagediv2"
id_textbox = "msdropdown20_titleText"
id_body = "pbox_body"
id_color = "pbox_color"
id_head = "pbox_head"
id_hand = "pbox_LH"
id_tail = "pbox_T"
id_fakemon_right_hand = "bbox_RH"
id_fakemon_left_hand  = "bbox_LH"
id_fakemon_tail  = "bbox_T"
id_fakemon_tail_icon = "bbox_img_T"
id_size = "numberSize"
id_position_x = "numberX"
id_remove = "removebtn"
class_selected = "selected"


default_tail_url = 'url("https://japeal.com/wordpress/wp-content/themes/total/PKM/imagefiles/SplitParts/Gen1_Originals_1.png")'
default_width = "70px"


def create_driver():
    driver = get_driver()
    print(" ")
    driver.set_window_position(60, 1)
    driver.set_window_size(744, 866)
    driver.get(fakemon_url)
    return driver


def init_website(driver:WebDriver):
    log("waiting for the default portrait to load")
    time.sleep(driver_delay)
    accept_all_cookies(driver)
    adapt_zoom(driver)
    clear_background(driver)
    log(" ")


def handle_body(driver:WebDriver, body:str):
    log("clicking on pokemon portrait")
    element_pokemon_selector = get_element_by_id(driver, id_pokemon_selector)
    element_pokemon_selector.click()
    time.sleep(basic_delay)

    log(f"writing pokemon name ({body})")
    element_textbox = get_element_by_id(driver, id_textbox)
    clear_element(element_textbox)
    element_textbox.send_keys(body)
    time.sleep(basic_delay)

    log("selecting the best choice")
    element_selected = get_element_by_class(driver, class_selected)
    element_selected.click()
    time.sleep(basic_delay)

    log("using new body")
    element_selected = get_element_by_id(driver, id_body)
    element_selected.click()
    time.sleep(basic_delay)


def handle_head(driver:WebDriver, head:str):
    log("clicking on pokemon portrait")
    element = get_element_by_id(driver, id_pokemon_selector)
    element.click()
    time.sleep(basic_delay)

    log(f"writing pokemon name ({head})")
    element = get_element_by_id(driver, id_textbox)
    # CRASHED HERE ONCE ALREADY, PERHAPS MORE DELAY COULD HELP
    clear_element(element)
    element.send_keys(head)
    time.sleep(basic_delay)

    log("selecting the best choice")
    element = get_element_by_class(driver, class_selected)
    element.click()
    time.sleep(basic_delay)

    log("using new color")
    element = get_element_by_id(driver, id_color)
    element.click()
    time.sleep(basic_delay)

    log("using new head")
    element = get_element_by_id(driver, id_head)
    element.click()
    time.sleep(basic_delay)

    log("using new hands")
    element = get_element_by_id(driver, id_hand)
    element.click()
    time.sleep(basic_delay)


    # checking if there is a tail, from the previous fusion
    element = get_element_by_id(driver, id_fakemon_tail_icon)
    element_width = element.value_of_css_property("width")
    element_bg = element.value_of_css_property("background-image")

    if element_width == default_width and element_bg != default_tail_url:
        log("selecting previous tail")
        element = get_element_by_id(driver, id_fakemon_tail)
        element.click()
        time.sleep(basic_delay)
        
        log("removing previous tail")
        element = get_element_by_id(driver, id_remove)
        element.click()
        time.sleep(basic_delay)

    log("using new tail")
    element = get_element_by_id(driver, id_tail)
    element.click()
    time.sleep(basic_delay)
    

def fix_rotom_cancer():
    log("using new right hand")
    element = get_element_by_id(driver, id_fakemon_right_hand)
    element.click()
    time.sleep(basic_delay)

    log("changing the size of the arm")
    element = get_element_by_id(driver, id_size)
    # CRASHED HERE ONCE ALREADY, PERHAPS MORE DELAY COULD HELP
    clear_element(element)
    element.send_keys("-22")
    time.sleep(basic_delay)

    log("changing the position of the arm")
    element = get_element_by_id(driver, id_position_x)
    clear_element(element)
    element.send_keys("30")
    time.sleep(basic_delay)

    log("using new left hand")
    element = get_element_by_id(driver, id_fakemon_left_hand)
    element.click()
    time.sleep(basic_delay)

    log("changing the position of the arm")
    element = get_element_by_id(driver, id_position_x)
    clear_element(element)
    element.send_keys("-30")
    time.sleep(basic_delay)


def create_fusion(driver:WebDriver, head:str, body:str):
    handle_body(driver, body)
    handle_head(driver, head)
    fix_rotom_cancer()

# head_list.append("Scizor")
head_list = []
head_list.append("Rhyperior") # have tail
head_list.append("Politoed") # have no tail
head_list.append("Magmortar") # tail-hand issue

# head_list.append("Wobbuffet")
# head_list.append("Weavile")
# head_list.append("Magby")
# head_list.append("Hitmontop")
# head_list.append("Elekid")
# head_list.append("Electivire")
# head_list.append("Delibird")
# head_list.append("Blaziken")
# head_list.append("Ambipom")


body = "Rotom"


driver = create_driver()
print("START")
init_website(driver)
for head in head_list:
    filename = f"{head}-{body}.png"
    print(filename)
    create_fusion(driver, head, body)
    print(driver.save_screenshot(f"new_rotom/{filename}"))
    print(" ")
# driver.close()
print("END")