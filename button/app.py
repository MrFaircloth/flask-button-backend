from flask import Flask, Response, request
from datetime import datetime, timedelta
from button_manager import Button
from groupme import post_to_groupme
from database import create_database, upsert_data, query_by_id, query_least_time_left

app = Flask(__name__)


HOURS_TOTAL = 336
HOURS_INTERVAL = 72
INTERVAL_COUNT = 10
BOT_ID = '1265f98891b058ffe37124304d'

button = Button('1m', '3s', 10, '0m')
game_over = False

# status_data = {
#     'alive': self._alive,
#     'current_interval': self.get_current_interval(),
#     'interval_count': self.interval_chunks_count,
#     'complete': self._is_complete(),
#     'time_alive': get_time_difference(self._init_date, datetime.now()),
# }


def query_button():
    global game_over
    ''' Function is repeatedly called to check the button status when not actively monitored. '''
    status = button.get_status()
    if game_over:
        return status

    if status.get('complete'):
        # send complete message
        message = 'The button has survived! The game is now over. Thank you for participating!'
        post_to_groupme(BOT_ID, message)
        game_over = True

    if not status.get('alive'):
        message = (
            'The button has died. The game is now over. Thank you for participating!'
        )
        post_to_groupme(BOT_ID, message)
        game_over = True
    return status


### Flask


@app.after_request
def add_cors_headers(response):
    # Replace '*' with the specific origin(s) you want to allow
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/')
def default():
    return 'button api'


@app.route('/ready')
def ready():
    return {'ready': True}


@app.route('/status')
def status():
    return query_button()

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
@app.route('/callback', methods=['POST'])
def callback():
    message_data: dict = request.get_json()
    if message_data.get('text') == '!save':
        status_before_save = button.get_status()
        alive = status_before_save['alive']
        complete = status_before_save['complete']

        if alive and not complete:
            button.reset()
            message = F"{message_data.get('name')} has saved the button."
            now = datetime.now()
            time_left: timedelta = button._interval_chunks[0] - now

            data = {
                "id": message_data.get('sender_id'),
                "name": message_data.get('name'),
                "last_saved": now,
                "interval": status_before_save.get('current_interval'),
                "time_left": time_left.seconds,
            }
            upsert_data(data)
            post_to_groupme(BOT_ID, message)
        else:
            message = (
                "Unfortunately, the button game is over. Thank you for participating!"
            )
            post_to_groupme(BOT_ID, message)

    # Return an acknowledgment response with a success status code (e.g., 200)
    return Response("Callback received and processed successfully.", status=200)


if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=5005)
