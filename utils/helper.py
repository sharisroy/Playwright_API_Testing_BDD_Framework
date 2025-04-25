import requests
from utils.data_loader import get_config
#
# # def login_user(email, password):
# #     config = get_config()
# #     url = config["base_url"] + "auth/login"
# #     headers = config["headers"]
# #     payload = {"userEmail": email, "userPassword": password}
# #     return requests.post(url, json=payload, headers=headers)
# #
# # def create_order(token, order):
# #     config = get_config()
# #     url = config["base_url"] + "orders/create-order"
# #     headers = {
# #         **config["headers"],
# #         "Authorization": token
# #     }
# #     payload = {"orders": [order]}
# #     return requests.post(url, json=payload, headers=headers)
#
#
# import requests
#
# def login_and_get_token(user_email, user_password):
#     from utils.data_loader import get_config
#     config = get_config()
#     base_url = config['base_url']
#     headers = config['headers']
#     url = base_url + "auth/login"
#
#     payload = {
#         "userEmail": user_email,
#         "userPassword": user_password
#     }
#
#     response = requests.post(url, json=payload, headers=headers)
#
#     if response.status_code == 200:
#         return response.json().get("token")
#     else:
#         return None

def login_and_get_token(user_email, user_password):
    from utils.data_loader import get_config
    config = get_config()
    base_url = config['base_url']
    headers = config['headers']
    url = base_url + "auth/login"

    payload = {
        "userEmail": user_email,
        "userPassword": user_password
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Login Response:", response.status_code, response.text)  # Add debug print

    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None
