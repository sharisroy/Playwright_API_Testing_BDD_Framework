import requests
from pytest_bdd import scenarios, given, when, then, parsers
from utils.data_loader import get_config, get_order_data

scenarios('../features/customer_order.feature')  # Link to the feature file

order_response = []

@given("I am authenticated with a valid user account")
def i_am_logged_in(auth_token):
    assert auth_token is not None     # Verify that the token is present

@when(parsers.parse('I request the details of my order'))
def get_order_details(auth_token, request):
    config = get_config()
    headers = {'Authorization': auth_token}

    response = requests.get(
        config["base_url"] + "order/get-orders-for-customer/67d8f80dc019fb1ad62b991d",
        headers=headers
    )
    order_response.append({
        "response": response
    })


@then("the order details should be successfully retrieved")
def verify_order_success():
    latest = order_response[-1]
    res = latest["response"]
    assert res.status_code == 200, f"Expected 200 but got {res.status_code}: {res.text}"
    # print(res.text)
    print(res.status_code)