# import json
# import os
#
# def get_config():
#     config_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'config.json')
#     with open(config_path, 'r') as file:
#         return json.load(file)
#
# def get_credentials():
#     credentials_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'credentials.json')
#     with open(credentials_path, 'r') as file:
#         return json.load(file)  # This returns the full dictionary
#
#

import json
import os

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def get_config():
    return load_json('data/config.json')

def get_credentials():
    return load_json('data/credentials.json')

def get_order_data():
    return load_json('data/test_data.json')
