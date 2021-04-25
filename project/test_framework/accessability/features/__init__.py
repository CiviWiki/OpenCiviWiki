from aloe import step

from .accessability import login, logout, is_user_loggedin


@step(r"a user with \"(.*?)\" credentials tries to log in")
def user_logs_in(self, correct):
    login(correct)


@step(r"the user is logged in")
def user_is_logged_in(self):
    assert is_user_loggedin()


@step(r"the user can log out")
def user_logs_out(self):
    logout()


@step(r"the user is not logged in")
def user_not_logged_in(self):
    assert not is_user_loggedin()
