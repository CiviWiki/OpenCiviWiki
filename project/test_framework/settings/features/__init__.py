import time
from selenium.webdriver.common.keys import Keys

from test_framework.utils import *
from test_framework.accessability.features import *
from test_framework.accessability.features.accessability import *


def open_menu(menu):
    find_element(nav_menu).click()
    if menu == "Settings":
        find_element(settings_button).click()
        wait_for_page("/settings")
    if menu == "My Profile":
        find_element(my_profile_button).click()
        wait_for_page(username)
    if menu == "My Feed":
        find_element(my_feed_button).click()


def get_settings():
    settings = {
        "email": world.browser.find_element_by_css_selector(email_field).get_attribute("value"),
        "username": world.browser.find_element_by_css_selector(username_field).get_attribute("value"),
        "first name": find_element(first_name_field).get_attribute("value"),
        "last name": find_element(last_name_field).get_attribute("value"),
        "location": find_element(location_field).text
    }
    return settings


def set_settings():
    time.sleep(1)
    first_name_1 = "unit"
    first_name_2 = "unit2"
    last_name_1 = "test"
    last_name_2 = "test2"
    location_1 = "Washington, DC, United States"
    location_2 = "New York, NY, United States"

    if find_element(first_name_field).get_attribute("value") == first_name_1:
        find_element(first_name_field).clear()
        find_element(first_name_field).send_keys(first_name_2)
    elif find_element(first_name_field).get_attribute("value") == first_name_2:
        find_element(first_name_field).clear()
        find_element(first_name_field).send_keys(first_name_1)

    if find_element(last_name_field).get_attribute("value") == last_name_1:
        find_element(last_name_field).clear()
        find_element(last_name_field).send_keys(last_name_2)
    elif find_element(last_name_field).get_attribute("value") == last_name_2:
        find_element(last_name_field).clear()
        find_element(last_name_field).send_keys(last_name_1)

    if location_1.replace(", DC, United States", "") in find_element(location_field).text:
        find_element(location_set).send_keys(location_2)
        time.sleep(1)
        find_element(location_set).send_keys(Keys.DOWN)
        find_element(location_set).send_keys(Keys.RETURN)
    elif location_2.replace(", NY, United States", "") in find_element(location_field).text:
        find_element(location_set).send_keys(location_1)
        time.sleep(1)
        find_element(location_set).send_keys(Keys.DOWN)
        find_element(location_set).send_keys(Keys.RETURN)

    find_element(first_name_field).click()


def is_activity_displayed():
    return find_element(activity).is_displayed()


def change_about_me():
    first_about = "this is the first about me string"
    second_about = "this is the secod about me string"
    find_element(edit_profile_butoon).click()
    about_me = find_element(about_me_field)
    world.first_about_me = about_me.get_attribute("value")

    if about_me.get_attribute("value") == first_about:
        about_me.clear()
        about_me.send_keys(second_about)
        about_me.send_keys(Keys.TAB)
    elif about_me.get_attribute("value") == second_about:
        about_me.clear()
        about_me.send_keys(first_about)
        about_me.send_keys(Keys.TAB)


def get_about_me():
    find_element(edit_profile_butoon).click()
    return find_element(about_me_field).get_attribute("value")


def is_my_feed_displayed():
    return find_element(my_feed_list).is_displayed()


def select_filter(filter):
    categories = find_elements_by_class("category-item")

    for category in categories:
        if category.text == filter:
            category.click()
            break


def get_threads_count():
    return len(find_elements_by_class("s12"))


def add_remove_category(mode, wanted_category):
    find_element(manage_categories).click()
    time.sleep(1)
    categories = find_elements_by_class("category-checkbox")
    for category in categories:
        if wanted_category in category.text:
            checkbox = category.find_element_by_class_name("filled-in")
            if mode == "remove" and checkbox.get_attribute("checked") == "true":
                category.find_elements_by_css_selector("*")[1].click()
                break
            elif mode == "add" and checkbox.get_attribute("checked") != "true":
                category.find_elements_by_css_selector("*")[1].click()
                break

    find_element(choose_button).click()
    time.sleep(3)


def find_category(wanted_category):
    categories = find_elements_by_class("category-item")
    for category in categories:
        if category.text == wanted_category:
            return "true"
    return


def is_trending_issues():
    return find_element(trending_issues).is_displayed()
