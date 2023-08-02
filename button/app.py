from flask import Flask, request
from button_manager import Button
from groupme import post_to_groupme

app = Flask(__name__)


HOURS_TOTAL = 336
HOURS_INTERVAL = 72
INTERVAL_COUNT = 10
button = Button('10m','20s', 10, '0m')
BOT_ID = ''


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
    return button.get_status()

# TODO: Handle "!save"
@app.route('/callback', methods=['POST'])
def callback():
    if request.method == 'POST':
        message_data: dict = request.get_json()
        if message_data.get('text') == '!save':
            status_before_save = button.get_status()
            button.reset()
            message = F"{message_data.get('name')} has saved the button at {status_before_save.get('current_interval')/{status_before_save.get('interval_count')}}"
            post_to_groupme(BOT_ID, message)
            


if __name__ == '__main__':
    # TODO: have a interval regularly poll the button
    # Save that output and use that in response ? 
    app.run(host='0.0.0.0', port=5005)
