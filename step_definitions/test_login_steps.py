import requests
from pytest_bdd import scenarios, given, when, then, parsers
from utils.data_loader import get_config, get_credentials

scenarios('../features/login.feature')

config = get_config()
credentials = get_credentials()["user_credentials"]
BASE_URL = config['base_url']
HEADERS = config['headers']

login_response = {}

@given("the API base url is loaded")
def api_base_url_loaded():
    return BASE_URL

@when(parsers.parse('I login using "{cred_type}" credentials'))
def login_with_credential(cred_type, request):
    cred = credentials[cred_type]
    payload = {
        "userEmail": cred["userEmail"],
        "userPassword": cred["userPassword"]
    }
    response = requests.post(BASE_URL + "auth/login", json=payload, headers=HEADERS)
    login_response["response"] = response

    # ✅ Attach data to HTML report
    for title, content in {
        "API Request Payload": payload,
        "API Response Body": response.text,
        "Status Code": response.status_code
    }.items():
        request.node._report_sections.append(("call", title, str(content)))

@then("the login should be successful")
def check_login_success():
    res = login_response["response"]
    assert res.status_code == 200
    assert "token" in res.json()

@then("the login should fail")
def check_login_failure():
    res = login_response["response"]
    msg = res.json().get("message", "").lower()
    assert res.status_code in [400, 401]
    assert any(err in msg for err in ["incorrect", "unauthorized", "login unsuccessful", "email is required"])
