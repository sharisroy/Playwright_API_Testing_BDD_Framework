Feature: Order Creation API Testing
  @smoke
  @regression
  @sanity
Scenario: Create order with valid product ID
    Given I am logged in with a valid user
    When I try to place an order using "valid_order" data
    Then the creation order should be successful

Scenario: Create order with invalid product ID
    Given I am logged in with a valid user
    When I try to place an order using "invalid_order" data
    Then the order creation should fail
