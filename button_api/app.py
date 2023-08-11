from flask import Flask, Response, request, jsonify

from button.button_manager import Button
from button.groupme import (
    post_to_groupme,
    callback_save,
    callback_score,
    callback_scoreboard,
)
from button.database import (
    create_database,
    query_get_leaderboard,
    get_latest_state,
    insert_button_state,
)
from button.util import results_to_dict

from button.config import config

app = Flask(__name__)

FLASK_PORT = config.FLASK_PORT
GROUPME_BOT_ID = config.GROUPME_BOT_ID
ALLOWED_ORIGINS = config.ALLOWED_ORIGINS
button = Button(
    config.TOTAL_TIME,
    config.INTERVAL_TIME_TOTAL,
    config.DEVIATION_TIME,
    config.INTERVAL_COUNT,
)

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
        post_to_groupme(GROUPME_BOT_ID, message)
        game_over = True

    if not status.get('alive'):
        message = (
            'The button has died. The game is now over. Thank you for participating!'
        )
        post_to_groupme(GROUPME_BOT_ID, message)
        game_over = True
    return jsonify(status)


### Flask
@app.after_request
def add_cors_headers(response):
    # Get the request's origin
    origin = request.headers.get('Origin')

    # Check if the request's origin is in the allowed list
    if origin in ALLOWED_ORIGINS:
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


@app.route('/debug')
def debug():
    debug_info = button.debug()
    data = results_to_dict(query_get_leaderboard())
    debug_info['leaderboard'] = data
    return jsonify(debug_info)


@app.route('/callback', methods=['POST'])
def callback():
    message_data: dict = request.get_json()
    text: str = message_data.get('text').lower()
    if text == '!save':
        callback_save(button, message_data)
    if text == '!score':
        callback_score(message_data)
    if text == '!dinosaur':
        callback_scoreboard(message_data)

    # Return an acknowledgment response with a success status code (e.g., 200)
    return Response("Callback received and processed successfully.", status=200)


def main():
    create_database()
    state = get_latest_state()
    if not state:
        insert_button_state(button)
    else:
        button._state_override(results_to_dict(state))
    app.run(host='0.0.0.0', port=FLASK_PORT)


if __name__ == '__main__':
    main()
