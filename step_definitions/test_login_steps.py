import requests
from pytest_bdd import scenarios, given, when, then, parsers
from utils.data_loader import get_credentials
from utils.helper import get_logger

scenarios('../features/login.feature')

logger = get_logger()
credentials = get_credentials()["user_credentials"]
login_response = {}

@given("the API base url is loaded")
def api_base_url_loaded(config):
    logger.info(f"Base URL: {config['base_url']}")
    return config["base_url"]

@when(parsers.parse('I login using "{cred_type}" credentials'))
def login_with_credential(cred_type, config):
    logger.info("Starting login test")

    cred = credentials[cred_type]
    payload = {
        "userEmail": cred["userEmail"],
        "userPassword": cred["userPassword"]
    }
    headers = config["headers"]
    url = config["base_url"] + config["login_endpoint"]

    logger.info(f"POST {url}")
    logger.info(f"Payload: {payload}")
    response = requests.post(url, json=payload, headers=headers)
    login_response["response"] = response

@then("the login should be successful")
def check_login_success():
    res = login_response["response"]
    assert res.status_code == 200, f"Expected 200 but got {res.status_code}: {res.text}"
    assert "token" in res.json(), "Token not found in response"

@then("the login should fail")
def check_login_failure():
    res = login_response["response"]
    msg = res.json().get("message", "").lower()
    assert res.status_code in [400, 401], f"Expected 400/401 but got {res.status_code}"
    assert any(err in msg for err in ["incorrect", "unauthorized", "login unsuccessful", "email is required"]), \
        f"Unexpected failure message: {msg}"
    logger.error("Message: %s", res.json().get("message", ""))
