import json

import pytest
import requests
from playwright.sync_api import APIRequestContext
from pytest_html import extras

from utils.data_loader import get_config, get_credentials, get_order_data

@pytest.fixture(scope="session")
def api_context(playwright):
    context = playwright.request.new_context(
        base_url="https://your-api-base-url.com",
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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call":
        response_text = getattr(item, "api_response_text", None)
        request_payload = getattr(item, "api_request_payload", None)
        status_code = getattr(item, "api_status_code", None)

        extra = getattr(rep, "extras", [])

        if status_code:
            extra.append(extras.text(f"Status Code: {status_code}", name="Status Code"))

        if request_payload:
            extra.append(extras.text(f"Request Payload:\n{request_payload}", name="Request Payload"))

        if response_text:
            extra.append(extras.text(f"Response Body:\n{response_text}", name="Response Body"))

        rep.extras = extra


@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    report.title = "Custom API Test Report"
    report.subtitle = "Playwright API Testing with a BDD Framework"

def pytest_metadata(metadata):
    metadata.clear()
    metadata["Project Name"] = "API Testing"
    metadata["Tester"] = "Haris"
    metadata["Environment"] = "Staging"
