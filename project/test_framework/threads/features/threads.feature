Feature: Threads tests

  Scenario: User can create threads
    Given a user with "correct" credentials tries to log in
    And user opens the "My Feed" menu
    When user can create a new "Federal" thread
    And user opens the "My Feed" menu
    And user can create a new "State" thread
    And user opens the "My Feed" menu
#    Then the user can delete a thread

  Scenario: User can add new problems, causes and solutions
    Given a user with "correct" credentials tries to log in
    And user opens the "My Feed" menu
    And the user opens the "automation Federal thread" thread
    When the user can add a "problem" to the thread
    And the user can add a "cause" to the thread
    And the user can add a "solution" to the thread

  Scenario: Civis are only visible when user votes AGREE
    Given a user with "correct" credentials tries to log in
    When the user opens the "automation Federal thread" thread
    Then the "cause" is "not visible" when user clicks "DISAGREE" on "this is a problem"
    And the "cause" is "visible" when user clicks "AGREE" on "this is a problem"
    And the "solution" is "not visible" when user clicks "DISAGREE" on "c1"
    And the "solution" is "visible" when user clicks "AGREE" on "c1"

  Scenario: User can add response to civis
    Given a user with "correct" credentials tries to log in
    When the user opens the "automation Federal thread" thread
    Then the user can add response to "this is a problem"

  Scenario: User can remove civis
    Given a user with "correct" credentials tries to log in
    When the user opens the "automation Federal thread" thread
    Then the user can remove "solution" called "this is a test solution"
    And the user can remove "cause" called "c1"
    And the user can remove "problem" called "this is a problem"