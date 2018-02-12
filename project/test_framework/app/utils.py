from aloe import world
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.hooks import with_chrome
from app.selectors import *

webDriverWaitInSeconds = 5


def open_home_page():
    world.browser.get(civi_wiki_url)
    wait_for_page(civi_wiki_url)



########################################################
# Waits for page with URL containing "url" to load
def wait_for_page(url):
    wait = WebDriverWait(world.browser, webDriverWaitInSeconds)
    wait.until(EC.url_contains(url))


# Returns a list of WebElement found by a CSS Selector
def find_elements(selector):
    return world.browser.find_elements_by_css_selector(selector)


# Returns a list of WebElement found by Class name
def find_elements_by_class(selector):
    return world.browser.find_elements_by_class_name(selector)


# Returns a single WebElement found by a CSS Selector
def find_element(selector):
    element = WebDriverWait(world.browser, webDriverWaitInSeconds).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    return element


# Returns a single WebElement found by Class name
def find_element_by_class(selector):
    return world.browser.find_element_by_class_name(selector)


# Returns a single WebElement found by Name
def find_element_by_name(selector):
    element = WebDriverWait(world.browser, webDriverWaitInSeconds).until(
        EC.element_to_be_clickable((By.NAME, selector)))
    return element


# Scrolls "element" into view. Used when element is outside the field of view
def scroll_into_view(element):
    world.browser.execute_script("arguments[0].scrollIntoView();", element)
    return element


# Uses JS to click on an "element". Used when "element" is not a button or text field
# Ex. homes in the Homes page
def js_click(element):
    world.browser.execute_script("arguments[0].click();", element)