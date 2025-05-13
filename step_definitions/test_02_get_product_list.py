from urllib import response

import pytest
import requests
from pytest_bdd import scenarios, given, parsers, when, then
from utils.helper import get_logger, get_auth_headers

scenarios('../features/get_product_list.feature')

logger = get_logger()
order_response = []

@given("I am authenticated with a valid user account")
def i_am_logged_in(user_obj):
    assert user_obj is not None

@when(parsers.parse('I request to get all product list'))
def get_product_list(user_obj, config):

    headers = get_auth_headers(user_obj['token'])
    url = config["base_url"] + config["all_product_endpoint"]

    product_response = requests.post(url, headers=headers)

    order_response.append(product_response.json())


@then("the product list should be successfully retrieved")
def verify_product_list(first_product):
    assert order_response, "No response received."

    response_data = order_response[0]

    assert response_data.get("message") == "All Products fetched Successfully"
    products = response_data.get("data", [])
    assert len(products) > 0, "Product list is empty"

    first_product.update(products[0])

    logger.info(f"First product: {first_product}")