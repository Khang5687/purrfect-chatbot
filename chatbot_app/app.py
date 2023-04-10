import os
import requests
from flask import Flask, request
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Replace with your own Facebook Page Access Token and Verify Token
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verify the webhook
        token_sent = request.args.get("hub.verify_token")
        if token_sent == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Invalid verification token"
    else:
        # Handle incoming messages
        output = request.get_json()
        print(f"Received payload: {output}")
        for event in output["entry"]:
            messaging = event["messaging"]
            for message in messaging:
                if "message" in message and "text" in message["message"]:
                    user_id = message["sender"]["id"]
                    user_name = get_user_name(user_id)
                    send_message(user_id, f"Hello, {user_name}!")

        return "Message processed", 200


def get_user_name(user_id):
    url = f"https://graph.facebook.com/{user_id}?fields=first_name,last_name&access_token={PAGE_ACCESS_TOKEN}"
    response = requests.get(url)
    user_data = response.json()
    return f"{user_data['first_name']} {user_data['last_name']}"


def send_message(recipient_id, text):
    data = {"recipient": {"id": recipient_id}, "message": {"text": text}}
    url = (
        f"https://graph.facebook.com/v16.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    )
    requests.post(url, json=data)
    # print("-----------------------")
    # print(response.content)


if __name__ == "__main__":
    app.run()
