<img align="center" src="https://raw.githubusercontent.com/jorge-jrzz/Pynani/main/docs/_static/banner-pynani-github.png" alt="banner Pynani">

---

Opensource python wrapper to Messenger API

## Features

### API

- Verify the webhook
- Send text messages
- Send attachments from a remote file (image, audio, video, file)
- Send attachments from a local file (image, audio, video, file)
- Send templates (generic, buttons, media, receipent)
- Send quick replies

### Other functionalities

- Get sender id
- Get type of message received
- Get text of the message received
- Get the url of the attachment received
- Get type of the attachment received
- Download attachments received

## Installation

Install Pynani with pip

```bash
  pip install pynani
```

Or install with pipenv (requires pipenv installed)

```bash
  pipenv install pynani
```

## Getting started

### Prerequisites

- **Python 3.8**+ installed
- To get started using this module, you will need **page access token** which you can get from the Facebook Developer Portal

### A simple echo bot

The Messenger class (defined in Messenger.py) encapsulates all API calls in a single class. It provides functions such as send_xyz (send_message, send_attachment etc.) and several ways to listen for incoming messages.

Create a file called echo_bot.py. Then, open the file and create an instance of the Messenger class.

```python
from pynani import Messenger

PAGE_ACCESS_TOKEN = 'EAAxxxxxxx...'
mess = Messenger(PAGE_ACCESS_TOKEN)
```

> [!IMPORTANT]
> Make sure to actually replace PAGE_ACCESS_TOKEN with your own page access token.

After that declaration, we need to register some message handlers. First, we need to create and verify a webhook with the help of _Flask_ or _FastAPI_.

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = "abc123"

@app.get("/")
def meta_verify():
    return mess.verify_token(request.args, TOKEN)
```

Now let's define a webhook that handles certain messages

```python
@app.post("/")
def meta_webhook():
    data = request.get_json()
    sender_id = mess.get_sender_id(data)
    message = mess.get_message_text(data)
    if message == "Hello":
        mess.send_text_message(sender_id, "Hello, World!")
    if message == "Bye":
        mess.send_text_message(sender_id, "Nice to meet you! 👍🏽")

    return jsonify({"status": "success"}), 200
```

We now have a basic bot which replies a static message to "hello" and "bye" messages. To start the bot, add the following to our source file:

```python
if __name__ =='__main__':
    app.run(port=8080, debug=True)
```

Alright, that's it! Our source file now looks like this:

```python
from flask import Flask, request, jsonify
from pynani import Messenger

PAGE_ACCESS_TOKEN = 'EAAxxxxxxx...'
TOKEN = "abc123"

mess = Messenger(PAGE_ACCESS_TOKEN)
app = Flask(__name__)

@app.get("/")
def meta_verify():
    return mess.verify_token(request.args, TOKEN)

@app.post("/")
def meta_webhook():
    data = request.get_json()
    sender_id = mess.get_sender_id(data)
    message = mess.get_message_text(data)
    if message == "Hello":
        mess.send_text_message(sender_id, "Hello, World!")
    if message == "Bye":
        mess.send_text_message(sender_id, "Nice to meet you! 👍🏽")

    return jsonify({"status": "success"}), 200

if __name__ =='__main__':
    app.run(port=8080, debug=True)
```

To start the bot, simply open up a terminal and enter `python echo_bot.py` to run the bot! Test it by sending messages ("hello" and "bye").

## Related

Here are some related projects that I was inspired by them.

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI?tab=readme-ov-file)
- [WhatsApp Cloud API Wrapper](https://github.com/Neurotech-HQ/heyoo)
- [Messenger API Python](https://github.com/krishna2206/messenger-api-python)
