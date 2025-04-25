
# Playwright API Testing Framework (BDD with Pytest)

This project is an **API testing automation framework** that uses **Playwright**, **Pytest**, and **pytest-bdd** to facilitate structured and behavior-driven testing for backend APIs. It offers robust features for testing API endpoints, managing test data, handling authentication, and generating detailed HTML reports.

## Features

- **BDD (Behavior Driven Development)** style testing using `pytest-bdd`
- **Playwright** for API context management and handling requests
- **Pytest** for test automation and report generation
- **pytest-html** for detailed HTML reports
- **Dynamic data loading** from JSON files for flexible test cases
- **Authentication** support with token management
- **Custom HTML reports** that display API request payloads, responses, and status codes
- **Modular test structure**, making it easy to add new endpoints or modify existing ones
- **Negative and positive test cases** for comprehensive API testing

## Technologies Used

- Python 3.x
- Playwright for API interactions
- Pytest for test automation
- pytest-bdd for BDD-style test scenarios
- pytest-html for detailed HTML reports
- JSON for test data and configuration management

## Project Structure

```
.
├── features/                       
│   ├── login.feature                 # Gherkin feature file for login functionality tests
│   ├── order.feature                 # Gherkin feature file for order creation tests
│   ├── customer_order.feature        # Gherkin feature file for customer order tests
│   ├── delete_order.feature          # Gherkin feature file for order deletion tests
│
├── step_definitions/                 
│   ├── test_login.steps.py           # Step definitions for login functionality tests
│   ├── test_order.steps.py           # Step definitions for order creation tests
│   ├── test_customer_order.steps.py  # Step definitions for customer order tests
│   ├── test_delete_order.steps.py    # Step definitions for order deletion tests
│
├── utils/                           
│   ├── data_loader.py                # Utility for loading test data
│   ├── helper.py                     # Helper functions for test support
│
├── data/                            
│   ├── credentials.json              # Sample credentials for login tests
│   ├── test_data.json                # Sample order data for order creation tests
│   ├── config.json                   # Configuration file with URL and other settings
│
├── reports/                          # Directory for storing test execution reports
├── conftest.py                       # Pytest fixtures and hooks (API context, auth tokens, etc.)
├── requirements.txt                  # Python dependencies for the project
├── pytest.ini                        # Pytest configuration file
└── .gitignore                        # Git ignore file to exclude unnecessary files

```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sharisroy/Playwright_API_Testing_BDD_Framework
   ```

2. **Install dependencies:**
   You can install the required Python packages using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API base URL and credentials**  
   Update the `config.json` or `data_loader.py` file to include your API base URL, login credentials, and any other necessary configurations.

4. **Run tests:**
   Once everything is set up, you can run your tests with Pytest:
   ```bash
   1. pytest
   2. pytest -n 4
   3. pytest -m smoke -v
   
   ```

## How It Works

1. **Login with valid credentials** to retrieve an authentication token.
2. **Place orders or delete orders** using the predefined scenarios in the `.feature` files.
3. **Validate responses** for each action (e.g., successful order creation, order deletion).
4. **Generate detailed HTML reports** after the test run for easy analysis.

## Example Scenario

Here’s an example scenario for placing an order:

```gherkin
Feature: Order Creation API Testing

  Scenario: Create order with valid product ID
    Given I am logged in with a valid user
    When I try to place an order using "valid_order" data
    Then the creation order should be successful

  Scenario: Create order with invalid product ID
    Given I am logged in with a valid user
    When I try to place an order using "invalid_order" data
    Then the order creation should fail
```

### Test Implementation

The test steps are defined using the **pytest-bdd** framework. For example, the following step verifies successful order creation:

```python
@then("the creation order should be successful")
def verify_create_order_success():
    res = order_response[-1]["response"]
    assert res.status_code == 201, f"Expected 201 but got {res.status_code}: {res.text}"
```

## Report Generation

Test reports are generated in **HTML format**, displaying the following details for each test run:
- **Request payload**
- **Response body**
- **Status code**

You can configure the report settings through the `pytest` configuration and customize it further.

## Contributing

Feel free to fork this repository, contribute with bug fixes or new features, and submit pull requests. All contributions are welcome!

---

### 🛠️ Future Improvements

- Support for additional API endpoints
- Enhanced error handling and retries
- Integration with CI/CD pipelines (GitHub Actions, Jenkins, etc.)
- More advanced reporting options (CSV, JUnit)

---

### 📄 License

This project is licensed under the MIT License.
