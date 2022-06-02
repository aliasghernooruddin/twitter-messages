import tweepy
from flask import Flask, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

consumer_key = os.environ.get('consumer_key')
consumer_secret = os.environ.get('consumer_secret')
access_token = os.environ.get('access_token')
access_token_secret = os.environ.get('access_token_secret')

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

app = Flask(__name__)
CORS(app)


@app.route('/')
def get_direct_messages():
    direct_messages = api.get_direct_messages()

    senders = []
    for messages in direct_messages:
        sender = messages.message_create['sender_id']
        name = get_user_name(sender)
        senders.append({'id': sender, 'name': name})

    response = {'status': 200, 'data': senders}
    return jsonify(response)


def get_user_name(id):
    user = api.get_user(user_id=id)
    return user.name
