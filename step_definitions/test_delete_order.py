from pytest_bdd import scenarios, given, when, then
import requests

from utils.data_loader import get_config
from utils.helper import get_logger, get_auth_headers

scenarios('../features/delete_order.feature')

delete_response = {}
logger = get_logger()


@given("I am authenticated with a valid user account")
def authenticated(user_obj):
    assert user_obj is not None


@when("I request to delete my order")
def delete_my_order(user_obj, latest_order_id, request):
    logger.info("Starting delete test")
    config = get_config()

    headers = get_auth_headers(user_obj["token"])

    delete_url = f"{config['base_url']}order/delete-order/{latest_order_id}"
    response = requests.delete(delete_url, headers=headers)

    delete_response["response"] = response


@then("the order should be successfully deleted")
def verify_delete_success():
    res = delete_response["response"]
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    logger.info("Message: {}".format(res.json()["message"]))
