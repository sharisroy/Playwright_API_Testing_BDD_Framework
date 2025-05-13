import requests
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from utils.data_loader import get_config, get_order_data
from utils.helper import get_logger, get_auth_headers

scenarios('../features/order.feature')

logger = get_logger()

@pytest.fixture
def order_context():
    return {}


@given("I am logged in with a valid user")
def i_am_logged_in(user_obj):
    assert user_obj is not None


@when(parsers.parse('I try to place an order using "{order_type}" data'))
def place_order(order_type, user_obj, order_context, config):
    logger.info("Starting create order test")

    # config = get_config()
    order_data = get_order_data()['order_list']
    headers = get_auth_headers(user_obj["token"])

    order = order_data.get(order_type)
    if not order:
        raise ValueError(f"Invalid order type: {order_type}")

    payload = {
        "orders": [order]
    }

    response = requests.post(
        config["base_url"] + config["order_endpoint"],
        json=payload,
        headers=headers
    )

    logger.info(f"Payload: {payload}")

    res_json = response.json()
    order_id = res_json.get("orders", [None])[0]

    order_context["order_type"] = order_type
    order_context["response"] = response
    order_context["order_id"] = order_id


@then("the creation order should be successful")
def verify_create_order_success(order_context):
    res = order_context["response"]
    assert res.status_code == 201, f"Expected 201 but got {res.status_code}: {res.text}"
    logger.info("Message: {}".format(res.json().get("message", "No message in response")))


@then("the order creation should fail")
def verify_order_creation_failure(order_context):
    res = order_context["response"]
    assert res.status_code in [400, 422], f"Expected failure status but got {res.status_code}: {res.text}"
    logger.error("---------- Create order failed ----------")
    logger.error("Message: %s", res.json().get("message", ""))
