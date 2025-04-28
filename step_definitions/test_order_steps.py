import requests
from pytest_bdd import scenarios, given, when, then, parsers
from utils.data_loader import get_config, get_order_data
from utils.helper import get_logger

scenarios('../features/order.feature')

order_response = []
logger = get_logger()

@given("I am logged in with a valid user")
def i_am_logged_in(auth_token):
    assert auth_token is not None

@when(parsers.parse('I try to place an order using "{order_type}" data'))
def place_order(order_type, auth_token, request):
    logger.info("Starting create order test")
    config = get_config()
    order_data = get_order_data()['order_list']
    headers = {'Authorization': auth_token}

    order = order_data.get(order_type)
    if not order:
        raise ValueError(f"Invalid order type: {order_type}")

    payload = {
        "orders": [order]
    }

    response = requests.post(
        config["base_url"] + "order/create-order",
        json=payload,
        headers=headers
    )
    # logger.info(f"Headers: {headers}")
    logger.info(f"Payload: {payload}")

    res_json = response.json()
    order_id = res_json.get("orders", [None])[0]

    order_response.append({
        "order_type": order_type,
        "response": response,
        "order_id": order_id
    })



@then("the creation order should be successful")
def verify_create_order_success():
    latest = order_response[-1]
    res = latest["response"]
    assert res.status_code == 201, f"Expected 201 but got {res.status_code}: {res.text}"
    logger.info("Message: {}".format(res.json()["message"]))
    # print(res.text)

@then("the order creation should fail")
def verify_order_creation_failure():
    latest = order_response[-1]
    res = latest["response"]
    assert res.status_code in [400, 422], f"Expected failure status but got {res.status_code}: {res.text}"
    logger.error("---------- Create order failed ----------")
    logger.error("Message: %s", res.json().get("message", ""))



