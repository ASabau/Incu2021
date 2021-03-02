#!/usr/bin/python3.8
import requests
from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI, Webhook
import time

app = Flask(__name__)

bot_token = "ZDg4YzlkZGMtZWY5Zi00MWJkLWIzN2MtM2ZiZTQ2ZmFmNzZkMzkzNjllYzItMjVh_PF84_consumer"
bot_name = "bazinga!@webex.bot"
previous_execution_time = 0

# create a connection object
api = CiscoSparkAPI(bot_token)


def get_chuck_norris_joke():
    '''
    Function which access the chuck norris jokes API and fetches a random joke
    '''
    chuck_url = "https://api.chucknorris.io/jokes/random"
    chuck_msg = requests.get(chuck_url)
    chuck_msg = chuck_msg.json()
    return chuck_msg['value']

@app.route("/", methods=['GET'])
def just_send_a_joke():
    return get_chuck_norris_joke()


@app.route("/", methods=['POST'])
def handle_message_and_send_joke():
    global previous_execution_time

    current_execution_time = time.time()
    if current_execution_time - previous_execution_time < 2:
        previous_execution_time = current_execution_time
        return

    previous_execution_time = current_execution_time # update the execution time of the function
    json_data = request.get_json()
    webhook_obj = Webhook(json_data)

    # Get the room details
    room = api.rooms.get(webhook_obj.data.roomId)

    # Get the message that was sent to the Bazinga bot
    message = api.messages.get(webhook_obj.data.id)

    if 'bazinga' not in message.text.lower():
        chuck_norris_joke = 'Sorry... You need to say the magic word "bazinga" for me to tell you a joke ;)'
    else:
        chuck_norris_joke = get_chuck_norris_joke()

    # Do not reply to the messages send by the bot in the chat
    if webhook_obj.data.personEmail != bot_name:
        # The message was not sent by the bazinga bot => reply with the Chuck Norris joke
        api.messages.create(room.id, text=chuck_norris_joke)