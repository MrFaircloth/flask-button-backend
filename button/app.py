from flask import Flask, request
from button import Button

app = Flask(__name__)


HOURS_TOTAL = 336
HOURS_INTERVAL = 72
INTERVAL_COUNT = 10
button = Button()


@app.route('/')
def default():
    return 'button api'


@app.route('/ready')
def ready():
    return {'ready': True}


@app.route('/status')
def status():
    current_interval = button.get_current_interval()
    return {
        'current_chunk': current_interval,
        'total_chunks': INTERVAL_COUNT,
    }


@app.route('/callback', methods=['POST'])
def callback():
    if request.method == 'POST':
        data = request.get_json()
        # Process the incoming data here
        print('Incoming POST data:', data)
        return 'POST request received successfully.'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
