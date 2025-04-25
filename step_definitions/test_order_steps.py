import requests
from pytest_bdd import scenarios, given, when, then, parsers
from utils.data_loader import get_config, get_order_data

scenarios('../features/order.feature')  # Link to the feature file

order_response = []

@given("I am logged in with a valid user")
def i_am_logged_in(auth_token):
    assert auth_token is not None     # Verify that the token is present

@when(parsers.parse('I try to place an order using "{order_type}" data'))
def place_order(order_type, auth_token, request):
    # Load the config and order data
    config = get_config()
    order_data = get_order_data()['order_list']  # Get the order data from JSON

    # Set headers for the API request
    headers = {'Authorization': auth_token}

    # Get the order data for the given order_type
    order = order_data.get(order_type)  # This retrieves the order based on the type passed
    if not order:
        raise ValueError(f"Invalid order type: {order_type}")  # Error if order type is invalid

    payload = {
        "orders": [order]  # Wrap the order in a list as required by the API
    }

    # Make the POST request to create the order
    response = requests.post(
        config["base_url"] + "order/create-order",  # Add the base URL and endpoint
        json=payload,
        headers=headers
    )


    # Store the response for further validation
    res_json = response.json()
    order_id = res_json.get("orders", [None])[0]
    order_response.append({
        "order_type": order_type,
        "response": response,
        "order_id": order_id
    })

    # 📝 Attach custom section in HTML report
    for title, content in {
        "API Request Payload": payload,
        "API Response Body": response.text,
        "Status Code": response.status_code
    }.items():
        request.node._report_sections.append(("call", title, str(content)))


@then("the creation order should be successful")
def verify_create_order_success():
    latest = order_response[-1]
    res = latest["response"]
    assert res.status_code == 201, f"Expected 201 but got {res.status_code}: {res.text}"
    # print(res.text)

@then("the order creation should fail")
def verify_order_creation_failure():
    latest = order_response[-1]
    res = latest["response"]
    assert res.status_code in [400, 422], f"Expected failure status but got {res.status_code}: {res.text}"



