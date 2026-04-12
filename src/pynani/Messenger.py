# ██████╗░██╗░░░██╗███╗░░██╗░█████╗░███╗░░██╗██╗
# ██╔══██╗╚██╗░██╔╝████╗░██║██╔══██╗████╗░██║██║
# ██████╔╝░╚████╔╝░██╔██╗██║███████║██╔██╗██║██║
# ██╔═══╝░░░╚██╔╝░░██║╚████║██╔══██║██║╚████║██║
# ██║░░░░░░░░██║░░░██║░╚███║██║░░██║██║░╚███║██║
# ╚═╝░░░░░░░░╚═╝░░░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝


import mimetypes
import json
from pathlib import Path
from typing import Union, Optional, Tuple, Dict, List
import requests
from requests.exceptions import RequestException
from .utils import get_logger


logger = get_logger(__name__)

HOOK_PAGE = """<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Verificación de Token</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      .container {
        max-width: 600px;
        margin: auto;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f9f9f9;
      }
      h1 {
        text-align: center;
      }
      p {
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Hello, World!</h1>
      <p>This is the endpoint to verify the token 🔐🔗</p>
    </div>
  </body>
</html>"""


def jsonify(data: Union[Dict, str], status_code: int) -> Tuple:
    """
    Converts the given data to a JSON response with the specified status code.

    Args:
        data (Union[Dict, str]): The data to be converted to JSON. It can be a dictionary or a string.
        status_code (int): The HTTP status code to be returned with the response.

    Returns:
        Tuple: A tuple containing the JSON response, the status code, and the headers.
    """

    if isinstance(data, dict):
        return json.dumps(data), status_code, {'Content-Type': 'application/json'}
    elif isinstance(data, str):
        return data.encode('utf-8'), status_code, {'Content-Type': 'text/html'}


def get_long_lived_token(app_id: str, app_secret: str, short_lived_token: str, save_env: Optional[bool] = False) -> Optional[str]:
    """
    Obtains a long-lived access token using the provided short-lived token.

    Args:
        app_id (str): The application ID.
        app_secret (str): The application secret.
        short_lived_token (str): The short-lived page access token.
        save_env (Optional[bool], optional): Whether to save the long-lived token to the .env file. Defaults to False.

    Returns:
        Optional[str]: The long-lived access token if successful, otherwise None.
    
    Exception:
        RequestException: If an error occurs during the request.
    
    Example:
        >>> get_long_lived_token('765xxx', 'e0fcxxx', 'EAAK4AXXXX', True)
        "EAAK4XXXX"
    """

    url = f"https://graph.facebook.com/v20.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={short_lived_token}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        logger.info("Long-lived token obtained successfully - %d", 200)
        if save_env:
            with open('.env', 'a', encoding='utf-8') as file:
                file.write(f'\nACCESS_TOKEN={r.json()["access_token"]}')
        return r.json()['access_token']
    except RequestException as e:
        logger.error("%s - %d", e, 403)
        return None


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


    def verify_token(self, params: Dict, token: str) -> Tuple:
        """
        Verifies the provided token against the expected token.

        Args:
            params (Dict): The parameters received in the verification request.
            token (str): The expected verification token.

        Returns:
            Tuple: A tuple containing the JSON response, the status code, and the headers.

        Example:
            >>> verify_token({"hub.mode": "subscribe", "hub.challenge": "1950414725", "hub.verify_token": "1234", }, "1234")
        Whit a Webhook made with Flask, the function verify_token() will be used as follows:
            >>> @app.get("/")
            >>> def meta_verify():
            >>>     return mess.verify_token(request.args, TOKEN)
        """

        mode = params.get("hub.mode")
        hub_token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge")

        if mode == "subscribe" and challenge:
            if hub_token != token:
                logger.error('Verification token mismatch - %d', 403)
                return jsonify({"Error": "Verification token mismatch"}, 403)
            logger.info('Verification successful - %d', 200)
            return jsonify(challenge, 200)
        logger.warning('This endpoint is to verify token - %d', 200,)
        return jsonify(HOOK_PAGE, 200)


    def get_sender_id(self, data: dict) -> Optional[str]:
        """
        Extracts the sender ID from the provided data.

        Args:
            data (dict): The data received from the webhook event.

        Returns:
            Optional[str]: The sender ID if found, otherwise None.
        
        Example with a Webhook made with Flask, will be used as follows:
            >>> get_sender_id(request.get_json())
            "1234567897654321"
        """

        try:
            return data['entry'][0]['messaging'][0]['sender']['id']
        except (IndexError, KeyError) as e:
            logger.error("Error accessing sender ID: %s", e)
            return None


    def get_message_type(self, data: Dict) -> Optional[str]:
        """
        Determines the type of message received from the webhook event.

        Args:
            data (Dict): The data received from the webhook event.

        Returns:
            Optional[str]: The type of message if found, otherwise None.
        
        Example with a Webhook made with Flask, will be used as follows:
            >>> get_message_type(request.get_json())
            "text"
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
            logger.error("Error accessing message type: %s", e)
            return None


    def get_message_text(self, data: Dict) -> Optional[str]:
        """
        Extracts the text message from the provided data.

        Args:
            data (Dict): The data received from the webhook event.

        Returns:
            Optional[str]: The text message if found, otherwise None.

        Example with a Webhook made with Flask, will be used as follows:
            >>> get_message_text(request.get_json())
            "Hello 👋🏽" 
        """

        try:
            message = data['entry'][0]['messaging'][0]
            if 'message' in message:
                return message['message']['text']
            elif 'postback' in message:
                return message['postback']['title']
        except (IndexError, KeyError) as e:
            logger.error("Error accessing message text: %s", e)
            return None


    def send_text_message(self, sender_id: str, message: Union[str, int]) -> Optional[Dict]:
        """
        Sends a text message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            message (Union[str, int]): The message to be sent.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.
        
        Example with a Webhook made with Flask, will be used as follows:
            >>> send_text_message(sender_id, "Hello, how can I help you?")
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
            logger.info("Message sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None


    def upload_attachment(self, attachment_type: str, attachment_path: str) -> str:
        """
        Uploads an attachment to the server and returns the attachment ID.

        Args:
            attachment_type (str): The type of the attachment (e.g., 'image', 'video', 'audio', 'file').
            attachment_path (str): The local file path to the attachment.

        Returns:
            str: The ID of the uploaded attachment if successful, otherwise None.
        
        Example with a Webhook made with Flask, will be used as follows:
            >>> upload_attachment("image", "path/to/image.png")
            "1234567897654321"
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
            r = requests.post(attachments_url, headers=header, files=file, data=body, timeout=20)
            r.raise_for_status()
            logger.info("Attachment uploaded successfully - %d", 200)
            attachment_id = r.json()["attachment_id"]
            return attachment_id
        except (RequestException, IndexError, KeyError) as e:
            logger.error("%s - %d", e, 403)
            return None


    def get_url_attachment(self, data: Dict) -> Optional[str]:
        """
        Extracts the URL of an attachment from the provided data.

        Args:
            data (Dict): The data containing the attachment information.

        Returns:
            Optional[str]: The URL of the attachment if found, otherwise None.
        
        Example with a Webhook made with Flask, will be used as follows:
            >>> get_url_attachment(request.get_json())
            "https://example.com/image.png"
        """

        try:
            return data['entry'][0]['messaging'][0]['message']['attachments'][0]["payload"]["url"]
        except (IndexError, KeyError) as e:
            logger.error("Error accessing attachment url: %s", e)
            return None


    def get_attachment_type(self, data: Dict) -> Optional[str]:
        """
        Extracts the type of an attachment from the provided data.

        Args:
            data (Dict): The data containing the attachment information.

        Returns:
            Optional[str]: The type of the attachment if found, otherwise None.

        Example with a Webhook made with Flask, will be used as follows:
            >>> get_attachment_type(request.get_json())
            "image"
        """

        try:
            return data['entry'][0]['messaging'][0]['message']['attachments'][0]["type"]
        except (IndexError, KeyError) as e:
            logger.error("Error accessing attachment type: %s", e)
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

        Example:
            >>> send_attachment(sender_id, "image", "https://example.com/image.png")
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
            logger.info("Attachment sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
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
        
        Example:
            >>> send_local_attachment(sender_id, "image", "path/to/image.png")
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
            logger.info("Attachment sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None


    def download_attachment(self, attachment_url: str, path_dest: str) -> None:
        """
        Downloads an attachment from the given URL and saves it to the specified destination path.

        Args:
            attachment_url (str): The URL of the attachment to be downloaded.
            path_dest (str): The local file path where the attachment will be saved.

        Returns:
            None

        Example:
            >>> download_attachment("https://example.com/image.png", "path/to/image.png")
        """

        try:
            r = requests.get(attachment_url, stream=True, timeout=10)
            r.raise_for_status()
            with open(path_dest, 'wb') as file:
                for chunk in r.iter_content(1024):
                    file.write(chunk)
            logger.info("Downloaded attachment successfully to \"%s\" - %d", path_dest, 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None
        

    def send_quick_reply(self, sender_id: str, message: Union[str, int], quick_replies: List[Dict]) -> Optional[Dict]:
        """
        Sends a quick reply message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            message (Union[str, int]): The message to be sent.
            quick_replies (list): A list of quick reply options. The list should contain less than 13 items.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.

        Example:
            >>> send_quick_reply(sender_id, "Select an option", [{'content_type': 'text', 'title': 'Hello', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': None}])
        Using the quick_buttons() function from pynani:
            >>> send_quick_reply(sender_id, "Select an option", quick_buttons(["Hello", "World", "💩"]))
        Usiing the quick_buttons_image() function from pynani:
            >>> send_quick_reply(sender_id, "Select an option", quick_buttons_image(["Hello", "World", "💩"], ["https://example.com/hello.png", "https://example.com/world.png", "https://example.com/poop.png"]))
        """

        if len(quick_replies) > 13:
            logger.warning("Quick replies should be less than 13")
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
            logger.info("Quick reply sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None


    def send_button_template(self, sender_id: str, message: str, buttons: List[Dict]) -> Optional[Dict]:
        """
        Sends a button template message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            message (str): The message to be sent.
            buttons (list): A list of button options. The list should contain less than 3 items.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.

        Example:
            >>> send_button_template(sender_id, "Select an option", [{'type': 'postback', 'title': 'Hello', 'payload': 'DEVELOPER_DEFINED_PAYLOAD', 'url': ''}])
        Using the basic_buttons() function from pynani:
            >>> send_button_template(sender_id, "Select an option", basic_buttons(["Hello", "World", "🤑"]))
        Using the exit_buttons() function from pynani:
            >>> send_button_template(sender_id, "Select an option", exit_buttons([{"title": "Exit", "url": "https://google.com"}, {"title": "Call me", "call_number": "+525555555555"}]))
        """

        if len(buttons) > 3:
            logger.warning("Buttons template should be less than 3")
            buttons = buttons[:3]

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
                        "template_type": "button",
                        "text": message,
                        "buttons": buttons
                    }
                }
            }
        }

        try:
            r = requests.post(self.__url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            logger.info("Button template sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None


    def send_media_template(self, sender_id: str, media_type: str, attachment_id: str, buttons: List[Dict]) -> Optional[Dict]:
        """
        Sends a media template message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            media_type (str): The type of media to be sent (e.g., 'image', 'video', 'audio', 'file').
            attachment_id (str): The ID of the attachment to be sent.
            buttons (list): A list of button options. The list should contain less than 3 items.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.
        
        Example:
            >>> send_media_template(sender_id, "image", "1234567897654321", [{'type': 'web_url', 'title': 'Hello', 'payload': '', 'url': 'https://example.com/hello.png'}])
        Using the basic_buttons() or exit_buttons() functions from pynani:
            >>> send_media_template(sender_id, "image", "1234567897654321", basic_buttons(["Hello", "World", "👻"]))
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

        try:
            r = requests.post(self.__url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            logger.info("Media template sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None


    def send_generic_template(self, sender_id: str, title: str, image_url: Optional[str] = None, default_url: Optional[str] = None,
                              subtitle: Optional[str] = None, buttons: Optional[List] = None) -> Optional[Dict]:
        """
        Sends a generic template message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            title (str): The title of the template.
            image_url (Optional[str], optional): The URL of the image to be displayed. Defaults to None.
            default_url (Optional[str], optional): The URL for the default action. Defaults to None.
            subtitle (Optional[str], optional): The subtitle of the template. Defaults to None.
            buttons (Optional[List], optional): A list of button options. Defaults to None.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.
        
        Example:
            >>> send_generic_template(sender_id, "Hello", "https://example.com/hello.png", "https://example.com", "World", [{'type': 'web_url', 'title': 'Hello', 'payload': '', 'url': 'https://example.com/hello.png'}])
        Using the basic_buttons() or exit_buttons() functions from pynani:
            >>> send_generic_template(sender_id, "Hello", "https://example.com/hello.png", "https://example.com", "World", basic_buttons(["Hello", "World", "👽"]))
        """

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
            r = requests.post(self.__url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            logger.info("Generic template sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None


    def send_receipt_template(self, sender_id: str, order_number: str, payment_method: str, summary: Dict, currency: str = 'USD',
                              order_url: Optional[str] = None, timestamp: Optional[str] = None, address: Optional[Dict] = None,
                              adjustments: Optional[List] = None, elements: Optional[List] = None) -> Optional[Dict]:
        """
        Sends a receipt template message to the specified sender.

        Args:
            sender_id (str): The ID of the recipient.
            order_number (str): The order number of the transaction.
            payment_method (str): The payment method used.
            summary (Dict): A dictionary containing the summary of the transaction.
            currency (str, optional): The currency used in the transaction. Defaults to 'USD'.
            order_url (Optional[str], optional): The URL of the order. Defaults to None.
            timestamp (Optional[str], optional): The timestamp of the transaction. Defaults to None.
            address (Optional[Dict], optional): The address of the recipient. Defaults to None.
            adjustments (Optional[List], optional): A list of adjustments made to the order. Defaults to None.
            elements (Optional[List], optional): A list of elements in the order. Defaults to None.

        Returns:
            Optional[Dict]: The response from the server if the request was successful, otherwise None.

        Example:
            >>> send_receipt_template(sender_id, "123456789", "Credit Card", 
                           {"subtotal": 75.00, 
                            "shipping_cost": 4.95, 
                            "total_tax": 6.19, 
                            "total_cost": 56.14},
                           "USD", "https://example.com/order/123456789", "123456789", 
                           {"street_1": "1 Hacker Way", 
                            "city": "Menlo Park", 
                            "postal_code": "94025", 
                            "state": "CA", 
                            "country": "US"},
                           [{"name": "New Customer Discount", "amount": 20}], 
                           [{"title": "Classic White T-Shirt", 
                             "subtitle": "100% Soft and Luxurious Cotton", 
                             "quantity": 2, "price": 50,
                             "currency": "USD", 
                             "image_url": "https://example.com/classic-white-t-shirt"}])
        Using the get_address(), get_summary(), get_adjustments(), and get_elements() functions from pynani:
            >>> address = get_address("123 Main St", "Springfield", "12345", "IL", "US")
            >>> adjustments = get_adjustments("New Customer Discount", 20, "Black Friday", 34)
            >>> summary = get_summary(56.14)
            >>> elements = get_elements("T-Shirt", 20.0)
            >>> send_receipt_template(sender_id, "123456789", "Credit Card", 
                           summary=summary,
                           currency="USD", 
                           order_url="https://example.com/order/123456789", 
                           timestamp="123456789", 
                           address=address,
                           adjustments=adjustments, 
                           elements=elements)
        """

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
            r = requests.post(self.__url, headers=header, json=body, timeout=10)
            r.raise_for_status()
            logger.info("Receipt template sent successfully - %d", 200)
            return jsonify(r.json(), 200)
        except RequestException as e:
            logger.error("%s - %d", e, 403)
            return None
