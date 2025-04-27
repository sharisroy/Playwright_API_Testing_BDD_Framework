Feature: Order Details Retrieval API Testing
  @smoke
  @regression
  Scenario: Retrieve order details with a valid order ID
    Given I am authenticated with a valid user account
    When I request the details of my order
    Then the order details should be successfully retrieved
