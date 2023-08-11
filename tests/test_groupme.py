import pytest
from unittest.mock import patch, Mock
from button_api.button.groupme import post_to_groupme  # Import the function you want to test


@pytest.fixture
def config():
    config = Mock()
    config.GROUPME_BOT_ID = '1234'
    config.GROUPME_ADMIN_USER_ID = '4567'
    config.DATABASE_URL = ''
    return config

@patch('button_api.button.config.config')
@patch('button_api.button.groupme.requests.post')
def test_post_to_groupme_successful(mock_post, config):
    # Mock the response to simulate a successful response
    mock_response = Mock()
    mock_response.status_code = 202
    mock_post.return_value = mock_response

    bot_id = 'your_bot_id'
    message = 'Test message'

    # Call the function
    post_to_groupme(bot_id, message)

    # Check if the mock function was called with the correct parameters
    mock_post.assert_called_once_with(
        'https://api.groupme.com/v3/bots/post',
        json={'bot_id': bot_id, 'text': message},
        headers={'Content-Type': 'application/json'}
    )

@patch('button_api.button.groupme.requests.post')
def test_post_to_groupme_failed(mock_post, config):
    # Mock the response to simulate a failed response
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = 'Internal Server Error'
    mock_post.return_value = mock_response

    bot_id = 'your_bot_id'
    message = 'Test message'

    # Call the function
    post_to_groupme(bot_id, message)

    # Check if the mock function was called with the correct parameters
    mock_post.assert_called_once_with(
        'https://api.groupme.com/v3/bots/post',
        json={'bot_id': bot_id, 'text': message},
        headers={'Content-Type': 'application/json'}
    )
