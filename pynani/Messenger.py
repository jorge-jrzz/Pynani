# ██████╗░██╗░░░██╗███╗░░██╗░█████╗░███╗░░██╗██╗
# ██╔══██╗╚██╗░██╔╝████╗░██║██╔══██╗████╗░██║██║
# ██████╔╝░╚████╔╝░██╔██╗██║███████║██╔██╗██║██║
# ██╔═══╝░░░╚██╔╝░░██║╚████║██╔══██║██║╚████║██║
# ██║░░░░░░░░██║░░░██║░╚███║██║░░██║██║░╚███║██║
# ╚═╝░░░░░░░░╚═╝░░░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝


import mimetypes
import json
import logging
from pathlib import Path
from typing import Union, Optional, Tuple, Dict
import requests
from requests.exceptions import RequestException


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s from Pynani - %(message)s'
)


def jsonify(data: Union[Dict, str], status_code: int) -> Tuple[Dict, int, Dict]:
    """
    Converts the given data to a JSON response with the specified status code.

    Args:
        data (Union[Dict, str]): The data to be converted to JSON. It can be a dictionary or a string.
        status_code (int): The HTTP status code to be returned with the response.

    Returns:
        Tuple[Dict, int, Dict]: A tuple containing the JSON response, the status code, and the headers.
    """

    if isinstance(data, dict):
        return json.dumps(data), status_code, {'Content-Type': 'application/json'}
    elif isinstance(data, str):
        return data.encode('utf-8'), status_code, {'Content-Type': 'text/html'}


class Messenger():
    """
    Initializes the Messenger class with the provided access token and page ID.

    Args:
        access_token (str): The access token for authenticating API requests.
        page_id (str, optional): The page ID for the Facebook page. Defaults to 'me'.
    """

    def __init__(self, access_token: str, page_id: str = 'me') -> None:
        self.access_token = access_token
        self.page_id = page_id
        self.__url = f"https://graph.facebook.com/v20.0/{page_id}/messages"


    def verify_token(self, params: Dict, token: str) -> Tuple[Dict, int, Dict]:
        """
        Verifies the provided token against the expected token.

        Args:
            params (Dict): The parameters received in the verification request.
            token (str): The expected verification token.

        Returns:
            Tuple[Dict, int, Dict]: A tuple containing the JSON response, the status code, and the headers.
        """

        mode = params.get("hub.mode")
        hub_token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and challenge:
            if hub_token != token:
                logging.info('Response: %d - %s', 403,
                             'Verification token mismatch')
                return jsonify("Verification token mismatch", 403)
            logging.info('Response: %d - %s', 200, "Verification successful")
            return jsonify(challenge, 200)
        logging.info('Response: %d - %s', 200,
                     "This endpoint is to verify token")
        return jsonify(Path("pynani/verify_token.html").read_text(encoding='utf-8'), 200)


    def get_sender_id(self, data: dict) -> Optional[str]:
        """
        Extracts the sender ID from the provided data.

        Args:
            data (dict): The data received from the webhook event.

        Returns:
            Optional[str]: The sender ID if found, otherwise None.
        """

        try:
            return data['entry'][0]['messaging'][0]['sender']['id']
        except (IndexError, KeyError) as e:
            logging.info("Error accessing sender ID: %s", e)
            return None


    def get_message_type(self, data: Dict) -> Optional[str]:
        """
        Determines the type of message received from the webhook event.

        Args:
            data (Dict): The data received from the webhook event.

        Returns:
            Optional[str]: The type of message if found, otherwise None.
        """

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
            logging.info("Error accessing message type: %s", e)
            # print(f"Error accessing message type: {e}")
            return None


    def get_message_text(self, data: Dict) -> Optional[str]:
        """
        Extracts the text message from the provided data.

        Args:
            data (Dict): The data received from the webhook event.

        Returns:
            Optional[str]: The text message if found, otherwise None.
        """

        try:
            message = data['entry'][0]['messaging'][0]
            if 'message' in message:
                return message['message']['text']
            elif 'postback' in message:
                return message['postback']['title']
        except (IndexError, KeyError) as e:
            logging.info("Error accessing message text: %s", e)
            # print(f"Error accessing message text: {e}")
            return None


    def send_text_message(self, sender_id: str, message: Union[str, int]) -> Optional[Dict]:
        """
        Sends a text message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            message (Union[str, int]): The message to be sent.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.
        """

        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        body = {
            "recipient": {
                "id": sender_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": message
            }
        }

        try:
            r = requests.post(self.__url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            logging.info("Response: %d - %s", 200, "Message sent successfully")
            return jsonify(r.json(), 200)
        except RequestException as e:
            logging.info("Response: %d - %s", 403, e)
            # print(f"Request failed: {e} \n{r.json()}")
            return None


    def upload_attachment(self, attachment_type: str, attachment_path: str) -> str:
        """
        Uploads an attachment to the server and returns the attachment ID.

        Args:
            attachment_type (str): The type of the attachment (e.g., 'image', 'video', 'audio', 'file').
            attachment_path (str): The local file path to the attachment.

        Returns:
            str: The ID of the uploaded attachment if successful, otherwise None.
        """

        attachments_url = f"https://graph.facebook.com/v20.0/{self.page_id}/message_attachments"
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

        try:
            r = requests.post(attachments_url, headers=header,
                              files=file, data=body, timeout=20)
            r.raise_for_status()
            logging.info("Response: %d - %s", 200,
                         "Attachment uploaded successfully")
            attachment_id = r.json()["attachment_id"]
            return attachment_id
        except (RequestException, IndexError, KeyError) as e:
            logging.info("Response: %d - %s", 403, e)
            # print(f"Request failed: {e} \n{r.json()}")
            return None


    def get_url_attachment(self, data: Dict) -> Optional[str]:
        """
        Extracts the URL of an attachment from the provided data.

        Args:
            data (Dict): The data containing the attachment information.

        Returns:
            Optional[str]: The URL of the attachment if found, otherwise None.
        """

        try:
            return data['entry'][0]['messaging'][0]['message']['attachments'][0]["payload"]["url"]
        except (IndexError, KeyError) as e:
            logging.info("Error accessing attachment url: %s", e)
            # print(f"Error accessing attachment url: {e}")
            return None


    def get_attachment_type(self, data: Dict) -> Optional[str]:
        """
        Extracts the type of an attachment from the provided data.

        Args:
            data (Dict): The data containing the attachment information.

        Returns:
            Optional[str]: The type of the attachment if found, otherwise None.
        """

        try:
            return data['entry'][0]['messaging'][0]['message']['attachments'][0]["type"]
        except (IndexError, KeyError) as e:
            logging.info("Error accessing attachment type: %s", e)
            # print(f"Error accessing attachment type: {e}")
            return None


    def send_attachment(self, sender_id: str, attachment_type: str, attachment_url: str) -> Optional[Dict]:
        """
        Sends an attachment to a user.

        Args:
            sender_id (str): The ID of the recipient.
            attachment_type (str): The type of the attachment (e.g., 'image', 'video', 'audio', 'file').
            attachment_url (str): The URL of the attachment to be sent.

        Returns:
            Optional[Dict]: The response from the server if the request is successful, otherwise None.
        """

        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        body = {
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

        try:
            r = requests.post(self.__url, headers=header, json=body, timeout=15)
            r.raise_for_status()
            logging.info("Response: %d - %s", 200, "Attachment sent successfully")
            return jsonify(r.json(), 200)
        except RequestException as e:
            logging.info("Response: %d - %s", 403, e)
            # print(f"Request failed: {e} \n{r.json()}")
            return None


    def send_local_attachment(self, sender_id: str, attachment_type: str, attachment_path: str) -> Optional[Dict]:
        """
        Sends a local attachment to a user.

        Args:
            sender_id (str): The ID of the recipient.
            attachment_type (str): The type of the attachment (e.g., 'image', 'video', 'audio', 'file').
            attachment_path (str): The local path to the attachment to be sent.

        Returns:
            Optional[Dict]: The response from the server if the request is successful, otherwise None.
        """

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

        try:
            r = requests.post(self.__url, headers=header, data=body, files=file, timeout=15)
            r.raise_for_status()
            logging.info("Response: %d - %s", 200, "Attachment sent successfully")
            return jsonify(r.json(), 200)
        except RequestException as e:
            logging.info("Response: %d - %s", 403, e)
            # print(f"Request failed: {e} \n{r.json()}")
            return None
        

    def download_attachment(self, attachment_url: str, path_dest: str) -> None:
        """
        Downloads an attachment from the given URL and saves it to the specified destination path.

        Args:
            attachment_url (str): The URL of the attachment to be downloaded.
            path_dest (str): The local file path where the attachment will be saved.

        Returns:
            None
        """

        try:
            r = requests.get(attachment_url, stream=True, timeout=10)
            r.raise_for_status()
            with open(path_dest, 'wb') as file:
                for chunk in r.iter_content(1024):
                    file.write(chunk)
            logging.info("Response: %d - Downloaded attachment successfully to %s", 200, path_dest)
        except RequestException as e:
            logging.info("Response: %d - %s", 403, e)
            return None


    def send_quick_reply(self, sender_id: str, message: Union[str, int], quick_replies: list) -> Optional[Dict]:
        """
        Sends a quick reply message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            message (Union[str, int]): The message to be sent.
            quick_replies (list): A list of quick reply options. The list should contain less than 13 items.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.
        """

        if len(quick_replies) > 13:
            logging.info("Quick replies should be less than 13")
            # print("Quick replies should be less than 13")
            quick_replies = quick_replies[:13]

        header = {"Content-Type": "application/json",
                  "Authorization": f"Bearer {self.access_token}"}
        body = {
            "recipient": {
                "id": sender_id
            },
            "messaging_type": "RESPONSE",
            "message": {
                "text": message,
                "quick_replies": quick_replies
            }
        }

        try:
            r = requests.post(self.__url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            logging.info("Response: %d - %s", 200, "Quick reply sent successfully")
            return jsonify(r.json(), 200)
        except RequestException as e:
            logging.info("Response: %d - %s", 403, e)
            return None

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

        r = requests.post(self.__url, headers=header, json=payload, timeout=10)
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

        r = requests.post(self.__url, headers=header, json=body, timeout=10)
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
            r = requests.post(self.__url, headers=header,
                              json=body, timeout=10)
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
            r = requests.post(self.__url, headers=header,
                              json=body, timeout=10)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e} \n{r.json()}")
            return None
