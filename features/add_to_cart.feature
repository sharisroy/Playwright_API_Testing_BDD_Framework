Feature: Add to Cart API Testing
  @smoke
  @regression
  Scenario: Add product to cart
    Given I am authenticated with a valid user account
    When I request add product to my cart
    Then the product added to my cart
