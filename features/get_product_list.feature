Feature: Product List Retrieval API Testing
  @regression
  Scenario: Retrieve Product List
    Given I am authenticated with a valid user account
    When I request to get all product list
    Then the product list should be successfully retrieved
