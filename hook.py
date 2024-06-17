from flask import Flask, request, jsonify
from pynani import Messenger, Buttons

PAGE_ACCESS_TOKEN = 'EAAOLpXLMAJABOwQ1aZCZAx8ksfLkia8fxmzkfJDFNzgB0A8pEzwAMLrlZCpv8VgS8Y58Cmimm9nlEA4x6pt8jaFlBEBdYXNT5FTfUgKcLu1Iqj9PzQR4jJE3PAwbjghWXSe2DsKDTyYZBxn26U78AO6FsBcrFYebZBvIZC1ZAfM4xN8aXPeRQdYY1jo8kXtShoG'
app = Flask(__name__)
mess = Messenger(PAGE_ACCESS_TOKEN)
b = Buttons()

@app.route("/", methods=['GET'])
def meta_verify():
    return mess.verify_token(request.args, '12345')

@app.route("/", methods=['POST'])
def meta_webhook():
    print("Algo paso!!!")
    data = request.get_json()
    mensaje = mess.get_message_text(data)
    print(mensaje)
    sender_id = mess.get_sender_id(data)
    if mensaje == "botones simples":
        botones = b.basic_buttons(["Opción 1", "Opción 2", "🔥"])
        mess.send_button_template(sender_id, "Hola, ¿qué deseas hacer?", botones)
    elif mensaje == "botones complicados":
        cb = b.leave_buttons([{'title': 'Opción 1', 'url': 'https://www.google.com'}, {'title': 'Opción 2', 'call_number': '+525555555555'}])
        mess.send_button_template(sender_id, "Hola, ¿qué deseas hacer?", cb)
    return jsonify({"status": "success"}), 200

if __name__ =='__main__':
    app.run(port=8080, debug=True)