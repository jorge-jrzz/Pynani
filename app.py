from flask import Flask, request, jsonify
from pynani import Messenger

PAGE_ACCESS_TOKEN = 'EAAL4nnkuqAcBO2quTrQj1ZCvCQU8owp5BBTSrJqh5clzX0gwHZADGTLQrvY6jGDoYW3ZBg8Y92lUR04YzaTow2ecjZCeeYJ1Vd8OM29t2wQi6eI8LpDlHZBxh24A2b1ZCdIaHs2lXyuTepOluyoIbaQNC7LSMueH9sB5twJoQXqlRF7pVkb5cMZBPzOZAR9lMAmd'
app = Flask(__name__)
mess = Messenger(PAGE_ACCESS_TOKEN)

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