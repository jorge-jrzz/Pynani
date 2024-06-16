from flask import Flask, request, jsonify
from pynani import Messenger

PAGE_ACCESS_TOKEN = 'EAAL4nnkuqAcBOZBzqEKtz4CUlGWBKDA6TntcHCiDRzo6xOteZA9qbei8fZBPpJuuO0aup5wZARLVZBcZBpkdEkJ9andibZBuxB7lTGaN6y064oAZAyV3ZB0fMuODe9ZB076BI6G529Id5Duo9gZCTYjWAWon86sveljMDQMXlhqyFZAtnTnErFDbbkllyOddG5IZBLCuG'
app = Flask(__name__)
mess = Messenger(PAGE_ACCESS_TOKEN)

@app.route("/", methods=['GET'])
def meta_verify():
    return mess.verify_token(request.args, '12345')

@app.route("/", methods=['POST'])
def meta_webhook():
    data = request.get_json()
    mt = mess.get_message_type(data)
    print(f"\n\n\nData received: \n{data}\nTipo del mensaje:{mt}\n\n")
    sender_id = mess.get_sender_id(data)
    print(f"Sender ID: {sender_id}")
    # mess.send_text_message(sender_id, "🔥")
    print("enviando archivo\n\n")
    reee = mess.send_local_attachment(sender_id, 'audio', '/Users/jorge-jrzz/Desktop/English/2 week/day 1/audio.m4a')
    print(f"Respuesta de envio de archivo: {reee}")
    return jsonify({"status": "success"}), 200

if __name__ =='__main__':
    app.run(port=8080, debug=True)