import logging

import requests
from utils.data_loader import get_config

def login_and_get_token(user_email, user_password):
    config = get_config()
    base_url = config['base_url']
    headers = config['headers']
    url = base_url + "auth/login"

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

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # you control what level of logs you want

    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add handler to logger
    if not logger.handlers:  # Prevent adding multiple handlers
        logger.addHandler(ch)

    return logger