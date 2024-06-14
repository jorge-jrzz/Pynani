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
    
    def get_url_attachment(self, data: dict):
        try:
            return data['entry'][0]['messaging'][0]['message']['attachments'][0]["payload"]["url"]
        except (IndexError, KeyError) as e:
            print(f"Error accessing attachment url: {e}")
            return None
        
    def get_attachment_type(self, data: dict):
        try:
            return data['entry'][0]['messaging'][0]['message']['attachments'][0]["type"]
        except (IndexError, KeyError) as e:
            print(f"Error accessing attachment type: {e}")
            return None
        
    def send_attachment(self, sender_id: str, attachment_type: str, attachment_url: str):
        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        payload = {
            "recipient":{
                "id":"24781539028157613"
            },
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                "type": attachment_type, 
                "payload": {
                    "url": attachment_url,
                    "is_reusable": True
                }
                }
            }
        }
        
        r = requests.post(self._url, headers=header, json=payload, timeout=10)
        return r.json()
    
    def download_attachment(self, attachment_url: str, path_dest: str):
        response = requests.get(attachment_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(path_dest, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            print('Downloaded attachment successfully!')
        else:
            print('Error downloading attachment')
    
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
