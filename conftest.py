import json
import logging
import pdb

import pytest
import requests
from playwright.sync_api import APIRequestContext, Playwright

from utils.data_loader import get_config, get_credentials

@pytest.fixture(scope="session")
def api_context(playwright: Playwright):
    context = playwright.request.new_context(
        extra_http_headers={
            "Content-Type": "application/json"
        }
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def auth_token(api_context: APIRequestContext):
    config = get_config()
    credentials = get_credentials()["user_credentials"]["valid_user"]

    login_url = config["base_url"] + "auth/login"
    payload = {
        "userEmail": credentials["userEmail"],
        "userPassword": credentials["userPassword"]
    }
    headers = config["headers"]

    response = api_context.post(
        login_url,
        data=json.dumps(payload),
        headers=headers
    )
    assert response.ok, f"Login failed: {response.status} - {response.text()}"
    # pdb.set_trace()
    token = response.json().get("token")
    assert token, "Token not found in login response"

    return token

@pytest.fixture(scope="module")
def latest_order_id(auth_token):
    config = get_config()
    headers = {'Authorization': auth_token}
    order_response = requests.get(config["base_url"] + "order/get-orders-for-customer/67d8f80dc019fb1ad62b991d",
                                  headers=headers)
    assert order_response.json()['message'] == "Orders fetched for customer Successfully"
    latest_order_id = order_response.json()['data'][0]['_id']
    return latest_order_id

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    report.title = "Custom API Test Report"
    report.subtitle = "Playwright API Testing with a BDD Framework"

def pytest_metadata(metadata):
    metadata.clear()
    metadata["Project Name"] = "API Testing"
    metadata["Tester"] = "Haris"
    metadata["Environment"] = "Staging"


def pytest_html_results_summary(prefix, summary, postfix):
    # Add custom CSS styles to the HTML report
    prefix.append(
        '''
        <style>
            /* Custom background color */
            body {
                background-color: #f4f4f9;
                font-family: Arial, sans-serif;
            }

            /* Modify the report title */
            h1 {
                color: #1a73e8;
                text-align: center;
                font-size: 2em;
            }

            /* Hide the default "Report generated on" section */
            p:contains("Report generated on") {
                # display: none;
            }

            /* Style for test summary */
            .summary td {
                padding: 10px;
                text-align: center;
            }

            /* Add a border to the table */
            table {
                border-collapse: collapse;
                width: 100%;
            }

            table, th, td {
                border: 1px solid #ccc;
            }

            th {
                background-color: #f0f0f0;
                color: #333;
                font-weight: bold;
            }

            /* Style for passed tests */
            .passed {
                background-color: #d4edda;
                color: #155724;
            }

            /* Style for failed tests */
            .failed {
                background-color: #f8d7da;
                color: #721c24;
            }

            /* Customize links in the report */
            a {
                color: #1a73e8;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }
        </style>
         <script>
            // JavaScript to hide the "Report generated on" section
            window.onload = function() {
                var reportText = document.querySelector("p");
                if (reportText && reportText.innerHTML.includes("Report generated on")) {
                    reportText.style.display = "none";
                }
            }
        </script>
        '''
    )
