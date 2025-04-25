Feature: Order Deletion API Testing






  Scenario: Delete an order with a valid order ID
    Given I am authenticated with a valid user account
    When I request to delete my order
    Then the order should be successfully deleted
