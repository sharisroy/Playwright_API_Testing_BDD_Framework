import datetime
import json
import logging
import pdb

import pytest
import requests
from playwright.sync_api import APIRequestContext, Playwright

from utils.data_loader import get_config, get_credentials


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",  # Default to dev if no env is passed
        help="Environment to run tests against: dev, qa, stage, prod"
    )


@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    with open("data/config.json") as f:
        full_config = json.load(f)

    if env not in full_config["environments"]:
        raise ValueError(f"Invalid environment: {env}")

    env_config = full_config["environments"][env]
    shared_config = full_config["shared"]

    # Merge shared and environment-specific settings
    merged_config = {
        "env": env,
        "base_url": env_config["base_url"],
        **shared_config
    }
    return merged_config


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
def user_obj(api_context: APIRequestContext, config):
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

    return response.json()

@pytest.fixture(scope="module")
def latest_order_id(user_obj, config):
    headers = {'Authorization': user_obj["token"]}
    url = f"{config['base_url']}order/get-orders-for-customer/{user_obj['userId']}"
    order_response = requests.get(url, headers=headers)

    assert order_response.ok, f"Failed to get order: {order_response.status_code}"
    assert order_response.json()['message'] == "Orders fetched for customer Successfully"

    return order_response.json()['data'][0]['_id']

@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    report.title = "Custom API Test Report"
    report.subtitle = "Playwright API Testing with a BDD Framework"

def pytest_metadata(metadata):
    metadata.clear()
    metadata["Project Name"] = "API Testing"
    metadata["Tester"] = "Haris"
    metadata["Environment"] = "Staging"

def pytest_configure(config):
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_name = f"report_{now}.html"
    config.option.htmlpath = f"reports/{report_name}"

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
