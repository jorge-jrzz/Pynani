from flask import Flask, request, jsonify
from pynani import Messenger

PAGE_ACCESS_TOKEN = '<PAGE_ACCESS_TOKEN>'
TOKEN = "<TOKEN>"

mess = Messenger(PAGE_ACCESS_TOKEN)
app = Flask(__name__)

@app.get("/")
def meta_verify():
    return mess.verify_token(request.args, TOKEN)

@app.post("/")
def meta_webhook():
    data = request.get_json()
    sender_id = mess.get_sender_id(data)
    if mess.get_message_type(data) == "text":
        message = mess.get_message_text(data)
        mess.send_text_message(sender_id, f"You said: {message}")

    return jsonify({"status": "success"}), 200

if __name__ =='__main__':
    app.run(port=8080, debug=True)
