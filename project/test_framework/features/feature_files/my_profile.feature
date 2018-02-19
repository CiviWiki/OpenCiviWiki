Feature: My Profile tests

  Scenario: User can change My Profile settings
    Given a user with "correct" credentials tries to log in
    When user opens the "My Profile" menu
    And the user can view it's activity
    Then the user can change About Me