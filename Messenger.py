import requests
from SocialMedia import SocialMedia


class Messenger(SocialMedia):
    def __init__(self, access_token):
        self._url = "https://graph.facebook.com/v20.0/me/messages"
        self.access_token = access_token

    def verify_token(self, params, token):
        mode = params.get("hub.mode")
        hub_token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and challenge:
            if hub_token != token:
                return "Verification token mismatch", 403
            return challenge, 200
        return "Hello world", 200

    def get_sender_id(self, data: dict):
        try:
            return data['entry'][0]['messaging'][0]['sender']['id']
        except (IndexError, KeyError) as e:
            print(f"Error accessing sender ID: {e}")
            return None

    def send_text_message(self, sender_id, message):
        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        payload = {
            "recipient": {
                "id": sender_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": message
            }
        }

        r = requests.post(self._url, headers=header, json=payload, timeout=10)
        return r.json()
