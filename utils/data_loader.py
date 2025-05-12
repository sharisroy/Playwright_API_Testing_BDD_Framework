import json

def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)

def get_config(env):
    config = load_json('data/config.json')

    if env not in config['environments']:
        raise ValueError(f"Invalid environment: {env}")

    merged = {
        "env": env,
        "base_url": config["environments"][env]["base_url"],
        **config["shared"]
    }
    return merged

def get_credentials():
    return load_json('data/credentials.json')

def get_order_data():
    return load_json('data/test_data.json')
