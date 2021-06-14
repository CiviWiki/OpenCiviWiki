import time
from selenium.webdriver.common.keys import Keys

from test_framework.utils import *
from test_framework.accessability.features import *


def open_thread(thread_name):
    time.sleep(3)
    threads = find_elements_by_class("thread-title")
    for thread in threads:
        if thread.text == thread_name:
            thread.click()
            wait_for_page("/thread/")
            break


def add_civi(mode, title, description, links):
    time.sleep(1)
    find_element(add_civi_button).click()
    if mode == "problem":
        find_element(add_problem_button).click()
        find_element(civi_title_field).send_keys(title)
        find_element(civi_description_field).send_keys(description)
    elif mode == "cause":
        find_element(add_cause_button).click()
        find_element(civi_title_field).send_keys(title)
        find_element(civi_description_field).send_keys(description)
        find_element(civi_links_field).send_keys(links)
        find_element(civi_links_field).send_keys(Keys.RETURN)
        time.sleep(1)
    elif mode == "solution":
        find_element(add_solution_button).click()
        find_element(civi_title_field).send_keys(title)
        find_element(civi_description_field).send_keys(description)
        find_element(civi_links_field).send_keys(links)
        find_element(civi_links_field).send_keys(Keys.RETURN)
        time.sleep(1)

    find_element(create_civi_button).click()
    return find_element(first_civi).is_displayed()


def create_thread(thread_type, title, summary, category):
    find_element(create_thread_button).click()
    find_element(thread_title).send_keys(title)
    find_element(thread_summary).send_keys(summary)
    find_element(thread_type_dropdown).click()

    for element in find_element(thread_type_dropdown).find_elements_by_css_selector(
        "*"
    ):
        if element.text == thread_type:
            element.click()
            break

    find_element(thread_category_dropdown).click()
    time.sleep(1)
    find_element(thread_category_dropdown).send_keys(Keys.DOWN)
    find_element(thread_category_dropdown).send_keys(Keys.RETURN)
    time.sleep(1)
    # for element in find_element_by_class("new-thread-category-selection").find_elements_by_css_selector("*"):
    #     if element.text in category:
    #         scroll_into_view(element)
    #         # js_click(element)
    #         element.click()
    #         break
    find_element(thread_create_draft).click()
    time.sleep(1)
    open_thread(title)
    find_element(thread_publish).click()
    time.sleep(3)


def civi_vote(civi_title, vote):
    for civi in find_elements_by_class("civi-card"):
        if civi_title in civi.find_element_by_class_name("text-wrapper").text:
            click_vote(vote, civi)


def click_vote(vote, element):
    options = element.find_elements_by_class_name("rating-wrapper")
    if vote == "DISAGREE":
        options[0].find_element_by_class_name("rating-button").click()
    elif vote == "NEUTRAL":
        options[2].find_element_by_class_name("rating-button").click()
    elif vote == "AGREE":
        options[4].find_element_by_class_name("rating-button").click()
    time.sleep(3)


def is_civi_visible(type):
    if type == "cause":
        number_of_elements = find_elements_by_class("cause-nav-indiv")
    elif type == "solution":
        number_of_elements = find_elements_by_class("solution-nav-indiv")
    elif type == "problem":
        number_of_elements = find_elements_by_class("problem-nav-indiv")

    if len(number_of_elements) > 0:
        return "true"
    else:
        return


def add_comment(civi_title, response_title_text, response_body_text):
    for civi in find_elements_by_class("civi-card"):
        if civi_title in civi.find_element_by_class_name("text-wrapper").text:
            # time.sleep(1)
            civi.click()
            # time.sleep(1)
            try:
                find_element(add_response_button).click()
            except:
                civi.click()
                find_element(add_response_button).click()
            find_element(response_title).send_keys(response_title_text)
            find_element(response_body).send_keys(response_body_text)
            find_element(response_confirm).click()
            # time.sleep(3)
            break


def remove_civi(civi_title):
    time.sleep(1)
    for civi in find_elements_by_class("civi-card"):
        if civi_title in civi.find_element_by_class_name("text-wrapper").text:
            try:
                civi.find_element_by_class_name("delete").click()
            except:
                time.sleep(2)
                civi.find_element_by_class_name("delete").click()
