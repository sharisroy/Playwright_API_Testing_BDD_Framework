import requests
from pytest_bdd import scenarios, when, given, then

from utils.helper import get_logger, get_auth_headers

scenarios('../features/add_to_cart.feature')
logger = get_logger()
cart_response = []


@given("I am authenticated with a valid user account")
def i_am_logged_in(user_obj):
    assert user_obj is not None

@when("I request add product to my cart")
def add_to_cart(user_obj, config, first_product):
    headers = get_auth_headers(user_obj['token'])
    url = config['base_url'] + config['add_to_cart_endpoint']
    payload = {
        "_id": user_obj['userId'],
        "product": first_product
    }

    response = requests.post(url, json=payload, headers=headers)
    logger.info(f"Add to cart response: {response.status_code} - {response.text}")
    cart_response.append(response.json())


@then("the product added to my cart")
def verify_product_added():
    assert cart_response, "No response stored from add-to-cart API"

    response_data = cart_response[0]
    assert response_data.get("message") == "Product Added To Cart", "Unexpected response message"
