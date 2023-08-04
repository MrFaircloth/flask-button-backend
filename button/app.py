import os
from flask import Flask, Response, request, jsonify
from datetime import datetime, timedelta
from button_manager import Button
from groupme import post_to_groupme
from database import create_database, upsert_data, query_by_id, query_get_leaderboard

app = Flask(__name__)


HOURS_TOTAL = 336
HOURS_INTERVAL = 72
INTERVAL_COUNT = 10
BOT_ID = os.getenv('GROUPME_BOT_ID')
if not BOT_ID:
    raise ValueError('Environment Variable: "GROUPME_BOT_ID" must be set.')
FLASK_PORT = os.getenv('FLASK_PORT', 5005)

button = Button('30d', '60h', 20)
game_over = False


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
    return jsonify(status)


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

@app.route('/debug')
def debug():
    debug_info = button.debug()
    data = [item.__dict__ for item in query_get_leaderboard()]
    # Remove the "_sa_instance_state" key from each dictionary
    data = [{k: v for k, v in item.items() if k != '_sa_instance_state'} for item in data]
    debug_info['leaderboard'] = data
    return jsonify(debug_info)

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
    app.run(host='0.0.0.0', port=FLASK_PORT)
