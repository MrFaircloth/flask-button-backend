import os
import yaml
import pytest
from button.config import AppConfig

@pytest.fixture
def config():
    # Create a temporary config.yaml for testing
    with open('test_config.yaml', 'w') as config_file:
        config_data = {
            'GROUPME_ADMIN_USER_ID': 1234,
            'GROUPME_BOT_ID': 'test_bot_id',
            'INTERVAL_COUNT': 25,
        }
        yaml.dump(config_data, config_file)
    
    yield AppConfig('test_config.yaml')

    # Clean up: Delete the temporary config.yaml
    os.remove('test_config.yaml')

def test_defaults(config):
    assert config.TOTAL_TIME == '30d'
    assert config.INTERVAL_TIME_TOTAL == '60h'
    assert config.FLASK_PORT == 5005
    assert config.ALLOWED_ORIGINS == ['http://66.27.115.160', 'https://anthonymastria.com']

def test_required_keys_present(config):
    assert hasattr(config, 'GROUPME_ADMIN_USER_ID')
    assert hasattr(config, 'GROUPME_BOT_ID')

def test_required_keys_missing():
    with open('test_config.yaml', 'w') as config_file:
        config_data = {
            'GROUPME_BOT_ID': 'test_bot_id',
        }
        yaml.dump(config_data, config_file)
        with pytest.raises(ValueError, match="Required configuration key 'GROUPME_ADMIN_USER_ID' is missing."):
            AppConfig('test_config.yaml')
    os.remove('test_config.yaml')

def test_custom_defaults(config):
    assert config.INTERVAL_COUNT == 25
    assert config.GROUPME_BOT_ID == 'test_bot_id'
