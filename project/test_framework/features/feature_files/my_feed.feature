Feature: My Feed tests

  Scenario: User can view My Feed
    Given a user with "correct" credentials tries to log in
    When user opens the "My Feed" menu
    And My Feed is displayed
    And user can filter threads by category
    And the user can "remove" the "Agriculture" category
    And the user can "add" the "Agriculture" category
    Then the trending issues are displayed