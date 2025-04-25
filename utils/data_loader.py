import json

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def get_config():
    return load_json('data/config.json')

def get_credentials():
    return load_json('data/credentials.json')

def get_order_data():
    return load_json('data/test_data.json')
