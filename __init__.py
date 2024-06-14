from flask import Flask, request, jsonify
from Pynani import Messenger, QuickReply

PAGE_ACCESS_TOKEN = 'EAAL4nnkuqAcBO0indBj1Q48sSf0TYZBu5KQYaKd4mvdAvjRn8IRsZCdZBVECTQZCGhgYBWQ2gdZAFokWw5PFDUo63mQ0f1pbr5zmLnmVWczOEKJcTX4ZCuZBzKDGWIBHDGoa6Qsa1ydvU1L7ZAHhtlEfToLHRUiZCHkfMXrqYPBCyvcdgXI9ncmeSbSnh3w7k7lM7'
app = Flask(__name__)
mess = Messenger.Messenger(PAGE_ACCESS_TOKEN)

@app.route("/", methods=['GET'])
def meta_verify():
    return mess.verify_token(request.args, '12345')

@app.route("/", methods=['POST'])
def meta_webhook():
    data = request.get_json()
    print(f"\n\n\nData received: \n{data}\n\n\n")
    sender_id = mess.get_sender_id(data)
    mess.send_text_message(sender_id, "👍🏽")

    return jsonify({"status": "success"}), 200

if __name__ =='__main__':
    app.run(port=8080, debug=True)