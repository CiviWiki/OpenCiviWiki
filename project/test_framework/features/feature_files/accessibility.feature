Feature: Accessibility  tests

  Scenario: A user can login and logout
    Given a user with "correct" credentials tries to log in
    When the user is logged in
    Then the user can log out

  Scenario: Users cannot login with wrong password
    Given a user with "incorrect" credentials tries to log in
    Then the user is not logged in