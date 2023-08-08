import yaml
import os, sys

class AppConfig:
    DEFAULTS = {
        'TOTAL_TIME': '30d',
        'INTERVAL_TIME_TOTAL': '60h',
        'INTERVAL_COUNT': 20,
        'FLASK_PORT': 5005,
        'ALLOWED_ORIGINS': ['http://66.27.115.160', 'https://anthonymastria.com'],
        'GROUPME_ADMIN_USER_ID': os.getenv('GROUPME_ADMIN_USER_ID'),
        'GROUPME_BOT_ID': os.getenv('GROUPME_BOT_ID'),
        'DATABASE_URL': os.getenv('DATABASE_URL'),
    }

    REQUIRED_KEYS = ['GROUPME_ADMIN_USER_ID', 'GROUPME_BOT_ID']

    def __init__(self, config_path='config.yaml'):
        config_path = os.getenv('BUTTON_CONFIG_YAML', config_path)
        self.config = self.DEFAULTS.copy()

        try:
            with open(config_path, 'r') as config_file:
                yaml_config = yaml.safe_load(config_file)

            if yaml_config:
                self.config.update(yaml_config)

        except FileNotFoundError:
            pass

        for key in self.REQUIRED_KEYS:
            if not self.config[key]:
                raise ValueError(f"Required configuration key '{key}' is missing.")

    def __getattr__(self, item):
        if item in self.config:
            return self.config[item]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

def create_config_instance() -> AppConfig:
    return AppConfig()

# Create the instance when not running under pytest
config = None
if 'pytest' not in sys.argv[0]:
    config = create_config_instance()