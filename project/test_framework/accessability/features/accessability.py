from test_framework.utils import *


def login(credentials):
    if is_user_loggedin():
        return
    else:
        open_home_page()
        el = find_element(login_signup_button)
        el.click()
        wait_for_page("login")
        find_element(username_field).send_keys(username)
        if credentials == "correct":
            find_element(password_field).send_keys(password)
            find_element(login_button).click()
        elif credentials == "incorrect":
            find_element(password_field).send_keys(password_wrong)


def is_user_loggedin():
    try:
        return find_element(user_label).is_displayed()
    except:
        return


def logout():
    find_element(nav_menu).click()
    find_element(logout_button).click()
