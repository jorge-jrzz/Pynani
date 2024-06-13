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
    

    