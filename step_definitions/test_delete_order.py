from pytest_bdd import scenarios, given, when, then
import requests

from utils.data_loader import get_config

scenarios('../features/delete_order.feature')

delete_response = {}


@given("I am authenticated with a valid user account")
def authenticated(auth_token):
    assert auth_token is not None


@when("I request to delete my order")
def delete_my_order(auth_token, latest_order_id, request):
    config = get_config()
    headers = {'Authorization': auth_token}

    delete_url = f"{config['base_url']}order/delete-order/{latest_order_id}"
    response = requests.delete(delete_url, headers=headers)

    delete_response["response"] = response
    print(delete_response)

    for title, content in {
        "Delete URL": delete_url,
        "Status Code": response.status_code,
        "Response Body": response.text
    }.items():
        request.node._report_sections.append(("call", title, str(content)))


@then("the order should be successfully deleted")
def verify_delete_success():
    res = delete_response["response"]
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
