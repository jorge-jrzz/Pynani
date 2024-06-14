import requests


class Messenger():
    def __init__(self, access_token: str, page_id: str = 'me'):
        self.access_token = access_token
        self.page_id = page_id
        self._url = f"https://graph.facebook.com/v20.0/{page_id}/messages"

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
        
    def get_message_text(self, data: dict):
        try:
            return data['entry'][0]['messaging'][0]['message']['text']
        except (IndexError, KeyError) as e:
            print(f"Error accessing message text: {e}")
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
    
    def send_quick_reply(self, sender_id, message: str, quick_replies: list):
        if len(quick_replies) > 13:
            print("Quick replies should be less than 13")
            quick_replies = quick_replies[:13]
        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        payload = {
            "recipient": {
                "id": sender_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": message,
                "quick_replies": quick_replies
            }
        }

        r = requests.post(self._url, headers=header, json=payload, timeout=10)
        return r.json()
