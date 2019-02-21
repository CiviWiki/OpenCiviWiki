Feature: Settings tests

  Scenario: User can change it's settings
    Given a user with "correct" credentials tries to log in
    When user opens the "Settings" menu
    And the current settings are saved
    And the user enters new settings
    Then the settings are changed