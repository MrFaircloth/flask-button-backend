import os
from flask import Flask, Response, request, jsonify
from datetime import datetime, timedelta
from button_manager import Button
from groupme import post_to_groupme
from database import create_database, upsert_data, query_by_id, query_get_leaderboard

app = Flask(__name__)


TOTAL_TIME = '30d'
INTERVAL_TIME_TOTAL = '60h'
INTERVAL_COUNT = 20
ADMIN_USER_ID='26159207'
BOT_ID = os.getenv('GROUPME_BOT_ID')
if not BOT_ID:
    raise ValueError('Environment Variable: "GROUPME_BOT_ID" must be set.')
FLASK_PORT = os.getenv('FLASK_PORT', 5005)

button = Button(TOTAL_TIME, INTERVAL_TIME_TOTAL, INTERVAL_COUNT)
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

allowed_origins = ['http://66.27.115.160', 'https://anthonymastria.com']

@app.after_request
def add_cors_headers(response):
    # Get the request's origin
    origin = request.headers.get('Origin')

    # Check if the request's origin is in the allowed list
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin


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

def _results_to_dict(query_results) -> dict:
    '''
    [{
        "interval": 20,
        "name": "Mitch",
        "saves_count": 1,
        "time_left": 215938,
        "last_saved": datetime.datetime(2023, 8, 4, 12, 17, 30, 602022),
        "id": "26159207"
    }]
    '''
    if not isinstance(query_results, list): query_results = [ query_results ]
    data = [item.__dict__ for item in query_results]
    # Remove the "_sa_instance_state" key from each dictionary
    data = [{k: v for k, v in item.items() if k != '_sa_instance_state'} for item in data]
    return data

@app.route('/debug')
def debug():
    debug_info = button.debug()
    data = _results_to_dict(query_get_leaderboard())
    debug_info['leaderboard'] = data
    return jsonify(debug_info)

def _callback_save(message_data: dict) -> None:
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
        post_to_groupme(BOT_ID, message)
    else:
        message = (
            "Unfortunately, the button game is over. Thank you for participating!"
        )
        post_to_groupme(BOT_ID, message)

def _callback_score(message_data: dict) -> None:

    user_id = message_data.get('sender_id')
    user_name = message_data.get('name')
    message = ''
    try: 
        data: dict = _results_to_dict(query_by_id(user_id))[0]
        message = f"{user_name} has a score of {data.get('interval')}"
    except:
        message = f'Failed to find score for user {user_name}.'
    post_to_groupme(BOT_ID, message)


def _callback_scoreboard(message_data: dict) -> None:
    user_id = message_data.get('sender_id')
    if user_id != ADMIN_USER_ID:
      return
    scoreboard_data = _results_to_dict(query_get_leaderboard())

    message = ''

    for item in scoreboard_data:
        formatted_time_left = f"{int(item['time_left'] / 60)} minutes"
        message += f"User: {item['name']}\nScore: {item['interval']}\nSave Count: {item['saves_count']}\nTime Left when Saved: {formatted_time_left}\n\n"


    post_to_groupme(BOT_ID, message)

@app.route('/callback', methods=['POST'])
def callback():
    message_data: dict = request.get_json()
    text: str = message_data.get('text').lower()
    if text == '!save':
        _callback_save(message_data)
    if text == '!score':
        _callback_score(message_data)
    if text == '!dinosaur':
        _callback_scoreboard(message_data)

    # Return an acknowledgment response with a success status code (e.g., 200)
    return Response("Callback received and processed successfully.", status=200)


if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=FLASK_PORT)
