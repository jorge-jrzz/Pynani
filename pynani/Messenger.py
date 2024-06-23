from typing import Union, Optional
from pathlib import Path
import mimetypes
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

    def get_message_type(self, data: dict):
        messaging = data['entry'][0]['messaging'][0]
        try:
            if 'postback' in messaging:
                return 'postback'
            message_type = messaging['message']
            if 'text' in message_type:
                if 'attachments' in message_type:
                    if message_type['attachments'][0]['type'] == 'fallback':
                        return 'link'
                return 'text'
            if 'attachments' in message_type:
                attachment_type = message_type['attachments'][0]['type']
                if 'image' in attachment_type:
                    if 'sticker_id' in message_type['attachments'][0]['payload']:
                        return 'sticker'
                    return 'image'
                else:
                    return attachment_type
        except (IndexError, KeyError) as e:
            print(f"Error accessing message type: {e}")
            return None

    def get_message_text(self, data: dict):
        try:
            message = data['entry'][0]['messaging'][0]
            if 'message' in message:
                # print("Hola?")
                return message['message']['text']
            elif 'postback' in message:
                return message['postback']['title']
        except (IndexError, KeyError) as e:
            print(f"Error accessing message text: {e}")
            return None

    def send_text_message(self, sender_id, message: Union[str, int]):
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

        try:
            r = requests.post(self._url, headers=header,
                              json=payload, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e} \n{r.json()}")
            return None

    def upload_attachment(self, attachment_type: str, attachment_path: str) -> str:
        attachments_url = f"https://graph.facebook.com/v20.0/{
            self.page_id}/message_attachments"
        attachment = Path(attachment_path)
        mimetype, _ = mimetypes.guess_type(attachment)

        header = {
            "Authorization": f"Bearer {self.access_token}"
        }
        message = {
            "attachment": {
                "type": attachment_type,
                "payload": {
                    "is_reusable": "true"
                }
            }
        }
        file = {
            "filedata": (attachment.name, attachment.open('rb'), mimetype)
        }
        body = {"message": str(message)}

        r = requests.post(attachments_url, headers=header,
                          files=file, data=body, timeout=20)

        try:
            attachment_id = r.json()["attachment_id"]
            return attachment_id
        except KeyError as e:
            print(f"Error uploading attachment: {e}")
            return None

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
            "recipient": {
                "id": sender_id
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

    def send_local_attachment(self, sender_id: str, attachment_type: str, attachment_path: str):
        attachment = Path(attachment_path)
        mimetype, _ = mimetypes.guess_type(attachment)
        recipient = {"id": sender_id}
        message = {
            "attachment": {
                "type": attachment_type,
                "payload": {
                    "is_reusable": "true"
                }
            }
        }

        header = {"Authorization": f"Bearer {self.access_token}"}
        body = {
            "recipient": str(recipient),
            "message": str(message)
        }
        file = {
            "filedata": (attachment.name, attachment.open('rb'), mimetype)
        }

        r = requests.post(self._url, headers=header,
                          data=body, files=file, timeout=10)
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

    def send_button_template(self, sender_id: str, message: str, buttons: list):
        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        payload = {
            "recipient": {
                "id": sender_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": message,
                        "buttons": buttons
                    }
                }
            }
        }

        r = requests.post(self._url, headers=header, json=payload, timeout=10)
        return r.json()

    def send_media_template(self, sender_id: str, media_type: str, attachment_id: str, buttons: list):
        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        body = {
            "recipient": {
                "id": sender_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [
                            {
                                "media_type": media_type,
                                "attachment_id": attachment_id,
                                "buttons": buttons
                            }
                        ]
                    }
                }
            }
        }

        r = requests.post(self._url, headers=header, json=body, timeout=10)
        return r.json()

    def send_generic_template(self, sender_id: str, title: str, image_url: Optional[str] = None, default_url: Optional[str] = None, subtitle: Optional[str] = None, buttons: Optional[list] = None):
        if default_url:
            default_action = {
                "type": "web_url",
                "url": default_url,
                "messenger_extensions": "false",
                "webview_height_ratio": "tall"
            }
        else:
            default_action = None

        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        body = {
            "recipient": {
                "id": sender_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": title,
                                "image_url": image_url if image_url else "",
                                "subtitle": subtitle if subtitle else "",
                                "default_action": default_action,
                                "buttons": buttons if buttons else []
                            }
                        ]
                    }
                }
            }
        }

        try:
            r = requests.post(self._url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e} \n{r.json()}")
            return None

    def send_receipt_template(self, sender_id: str, order_number: str, payment_method: str, summary: dict, currency: str = 'USD',
                              order_url: Optional[str] = None, timestamp: Optional[str] = None, address: Optional[dict] = None,
                              adjustments: Optional[list] = None, elements: Optional[list] = None):
        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        body = {
            "recipient": {
                "id": sender_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "receipt",
                        "recipient_name": "Stephane Crozatier",
                        "order_number": order_number,
                        "currency": currency,
                        "payment_method": payment_method,
                        "order_url": order_url,
                        "timestamp": timestamp,
                        "address": address,
                        "summary": summary,
                        "adjustments": adjustments,
                        "elements": elements
                    }
                }
            }
        }

        try:
            r = requests.post(self._url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e} \n{r.json()}")
            return None
