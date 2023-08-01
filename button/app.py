from flask import Flask, request
from button import Button

app = Flask(__name__)


HOURS_TOTAL = 336
HOURS_INTERVAL = 72
INTERVAL_COUNT = 10
button = Button('10m','20s', 10, '0m')


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
        data = request.get_json()
        # Process the incoming data here
        print('Incoming POST data:', data)
        return 'POST request received successfully.'


if __name__ == '__main__':
    # TODO: have a interval regularly poll the button
    # Save that output and use that in response ? 
    app.run(host='0.0.0.0', port=5005)
