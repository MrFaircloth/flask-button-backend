import requests

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
        print('Message sent successfully!')
    else:
        print(
            f'Failed to send message. Status code: {response.status_code}, Response: {response.text}'
        )
