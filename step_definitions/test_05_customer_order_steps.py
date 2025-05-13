import requests
from pytest_bdd import scenarios, given, when, then, parsers
from utils.helper import get_logger, get_auth_headers

scenarios('../features/customer_order.feature')

order_response = []
logger = get_logger()

@given("I am authenticated with a valid user account")
def i_am_logged_in(user_obj):
    assert user_obj is not None     # Verify that the token is present

@when(parsers.parse('I request the details of my order'))
def get_order_details(user_obj, config):
    logger.info("Starting get order details test")

    headers = get_auth_headers(user_obj["token"])
    url = config["base_url"] + "order/get-orders-for-customer/" + user_obj["userId"]

    logger.info(f"GET {url}")
    response = requests.get(url, headers=headers)

    order_response.append({
        "response": response
    })

@then("the order details should be successfully retrieved")
def verify_order_success():
    latest = order_response[-1]
    res = latest["response"]
    assert res.status_code == 200, f"Expected 200 but got {res.status_code}: {res.text}"
    logger.info("Message: {}".format(res.json()["message"]))