import logging
import requests

def login_and_get_token(user_email, user_password, config):
    base_url = config['base_url']
    headers = config['headers']
    url = base_url + config["login_endpoint"]

    payload = {
        "userEmail": user_email,
        "userPassword": user_password
    }

    response = requests.post(url, json=payload, headers=headers)
    print("Login Response:", response.status_code, response.text)

    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None

def get_auth_headers(token: str):
    return {
        'Authorization': f"{token}",
        'Content-Type': 'application/json'
    }

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)


    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(ch)

    return logger