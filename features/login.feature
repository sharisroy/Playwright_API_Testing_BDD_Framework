Feature: User Login API Testing

  Scenario: Successful login with valid credentials
    Given the API base url is loaded
    When I login using "valid_user" credentials
    Then the login should be successful

  Scenario: Login with invalid password
    Given the API base url is loaded
    When I login using "invalid_password" credentials
    Then the login should fail

  Scenario: Login with wrong password
    Given the API base url is loaded
    When I login using "wrong_password" credentials
    Then the login should fail

  Scenario: Login with empty email
    Given the API base url is loaded
    When I login using "empty_email" credentials
    Then the login should fail

  Scenario: Login with invalid email format
    Given the API base url is loaded
    When I login using "invalid_email" credentials
    Then the login should fail
