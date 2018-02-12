from aloe import step

from app.tasks.settings_tasks import *


@step(r'user opens the \"(.*?)\" menu')
def user_opens_menu(self, menu):
    open_menu(menu)


@step(r'the current settings are saved')
def current_settings_are_saved(self):
    world.old_settings = get_settings()


@step(r'the user enters new settings')
def user_enters_settings(self):
    set_settings()
    # time.sleep(3)


@step(r'the settings are changed')
def settings_are_changed(self):
    open_home_page()
    open_menu("Settings")
    new_settings = get_settings()
    assert new_settings.get("email") == world.old_settings.get("email")
    assert new_settings.get("username") == world.old_settings.get("username")
    assert not new_settings.get("first name") == world.old_settings.get("first name")
    assert not new_settings.get("last name") == world.old_settings.get("last name")
    assert not new_settings.get("location") == world.old_settings.get("location")


@step(r'the user can view it\'s activity')
def user_can_view_activity(self):
    assert is_activity_displayed()


@step(r'the user can change About Me')
def user_can_change_aboutme(self):
    change_about_me()
    open_home_page()
    open_menu("My Profile")

    assert not world.first_about_me == get_about_me()


@step(r'My Feed is displayed')
def my_feed_is_displayed(self):
    assert is_my_feed_displayed()


@step(r'user can filter threads by category')
def user_can_filter_threads(self):
    select_filter("All")
    initial_count = get_threads_count()
    select_filter("Environment")
    actual_count = get_threads_count()
    assert not initial_count == actual_count


@step(r'the user can \"(.*?)\" the \"(.*?)\" category')
def user_removes_category(self, mode, category):
    if mode == "remove":
        add_remove_category(mode, category)
        assert not find_category(category)
    elif mode == "add":
        add_remove_category(mode, category)
        assert find_category(category)


@step(r'the trending issues are displayed')
def trending_issues_are_displayed(self):
    assert is_trending_issues()