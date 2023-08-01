import requests
from flask import Flask, request

app = Flask(__name__)

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

@app.route('/')
def home():
    return 'Hello, World! This is your Flask app listening on port 5000.'

@app.route('/callback', methods=['POST'])
def incoming():
    if request.method == 'POST':
        data = request.get_json()
        # Process the incoming data here
        print('Incoming POST data:', data)
        return 'POST request received successfully.'

if __name__ == '__main__':
    app.run(host='localhost', port=5002)

def post_to_groupme_bot(bot_id, message):
    url = 'https://api.groupme.com/v3/bots/post'
    headers = {'Content-Type': 'application/json'}
    data = {
        'bot_id': bot_id,
        'text': message
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 202:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')

# Example usage:
# Replace 'YOUR_BOT_ID' with the actual bot ID and 'Hello world' with the message you want to send.
# bot_id = '08b7604f86be15edec9b597d4c'
# message = 'Hello world'

# post_to_groupme_bot(bot_id, message)