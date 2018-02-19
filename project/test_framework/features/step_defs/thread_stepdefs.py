from aloe import step

from app.tasks.thread_tasks import *


@step(r'the user opens the \"(.*?)\" thread')
def user_opens_thread(self, thread_name):

    open_thread(thread_name)


@step(r'the user can add a \"(.*?)\" to the thread')
def user_can_add_to_thread(self, mode):
    if mode == 'problem':
        title = "this is a problem"
        description = "this is a problem description"
        links = ""
    elif mode == "cause":
        title = "c1"
        description = "this is a cause description"
        links = "problem"
    elif mode == "solution":
        title = "this is a test solution"
        description = "this is a cause solution"
        links = "c1"
        time.sleep(3)

    assert add_civi(mode, title, description, links)


@step (r'user can create a new \"(.*?)\" thread')
def user_can_create_thread(self, thread_type):
    thread_title = "automation " + thread_type + " thread"
    summary = "thread summary"
    category = "Environment"
    create_thread(thread_type, thread_title, summary, category)


@step(r'the \"(.*?)\" is \"(.*?)\" when user clicks \"(.*?)\" on \"(.*?)\"')
def user_can_view_civis(self, civi_type, visibility, vote, parent_name):
    civi_vote(parent_name, vote)
    if visibility == "not visible":
        assert not is_civi_visible(civi_type)
    elif visibility == "visible":
        assert is_civi_visible(civi_type)


@step(r'the user can add response to \"(.*?)\"')
def user_can_add_comment(self, civi_title):
    response_title = "this is a response title"
    response_body = "this is a response body"
    add_comment(civi_title, response_title, response_body)

@step(r'the user can remove \"(.*?)\" called \"(.*?)\"')
def user_can_remove_civi(self, type, civi_title):
    remove_civi(civi_title)
    assert is_civi_visible(type)