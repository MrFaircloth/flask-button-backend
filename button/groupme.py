import requests
from datetime import datetime, timedelta

from util import results_to_dict
from database import query_get_leaderboard, upsert_data, query_by_id
from button_manager import Button
from config import config

GROUPME_BOT_ID = config.GROUPME_BOT_ID
GROUPME_ADMIN_USER_ID = config.GROUPME_ADMIN_USER_ID


''' Sample callback
{
  "attachments": [],
  "avatar_url": "https://i.groupme.com/123456789",
  "created_at": 1302623328,
  "group_id": "1234567890",
  "id": "1234567890",
  "name": "John",
  "sender_id": "12345",
  "sender_type": "user",
  "source_guid": "GUID",
  "system": false,
  "text": "Hello world ☃☃",
  "user_id": "1234567890"
}
'''

def post_to_groupme(bot_id, message):
    url = 'https://api.groupme.com/v3/bots/post'
    headers = {'Content-Type': 'application/json'}
    data = {'bot_id': bot_id, 'text': message}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 202:
        print(f'Sent: {message}')
    else:
        print(
            f'Failed to send message. Status code: {response.status_code}, Response: {response.text}'
        )


# CALLBACK HANDLERS

def callback_save(button: Button, message_data: dict) -> None:
    status_before_save = button.get_status()
    alive = status_before_save['alive']
    complete = status_before_save['complete']

    if alive and not complete:
        now = datetime.now()
        time_left: timedelta = int((button._interval_chunks[0] - now).total_seconds())
        button.reset()
        message = F"{message_data.get('name')} has saved the button."

        data = {
            "id": message_data.get('sender_id'),
            "name": message_data.get('name'),
            "last_saved": now,
            "interval": status_before_save.get('current_interval'),
            "time_left": time_left,
        }
        upsert_data(data)
        post_to_groupme(GROUPME_BOT_ID, message)
    else:
        message = (
            "Unfortunately, the button game is over. Thank you for participating!"
        )
        post_to_groupme(GROUPME_BOT_ID, message)

def callback_score(message_data: dict) -> None:

    user_id = message_data.get('sender_id')
    user_name = message_data.get('name')
    message = ''
    try: 
        data: dict = results_to_dict(query_by_id(user_id))[0]
        message = f"{user_name} has a score of {data.get('interval')}"
    except:
        message = f'Failed to find score for user {user_name}.'
    post_to_groupme(GROUPME_BOT_ID, message)


def callback_scoreboard(message_data: dict) -> None:
    user_id = message_data.get('sender_id')
    if user_id != GROUPME_ADMIN_USER_ID:
      return
    scoreboard_data = results_to_dict(query_get_leaderboard())

    message = ''

    for item in scoreboard_data:
        formatted_time_left = f"{int(item['time_left'] / 60)} minutes"
        message += f"User: {item['name']}\nScore: {item['interval']}\nSave Count: {item['saves_count']}\nTime Left when Saved: {formatted_time_left}\n\n"


    post_to_groupme(GROUPME_BOT_ID, message)