from flask import Flask, request, jsonify
from pynani import Messenger, Buttons

PAGE_ACCESS_TOKEN = 'EAAL4nnkuqAcBO7WJZBbXWineRCJaQv3yvPL3DfzQyrmV6PiUNYrTxxHuZC7S3bWC2fnzGwaxNR5uPJ4OhuEOKpvBensrlHPId6pXHdOZBw4J70RC1jgRhhp9137TgoGRSlpZAdZCHAeBwmloZBqGWNmLUv9CPkHYUY6iIqx23SuOQu1sdghVOnmjSDr0qBc9ol'
app = Flask(__name__)
mess = Messenger(PAGE_ACCESS_TOKEN)
b = Buttons()

@app.route("/", methods=['GET'])
def meta_verify():
    return mess.verify_token(request.args, '12345')

@app.route("/", methods=['POST'])
def meta_webhook():
    # print("Algo paso!!!")
    data = request.get_json()
    mensaje = mess.get_message_text(data)
    # print(f'\nData: {data}\n')
    # print(mensaje)
    # print(mess.get_message_type(data))
    sender_id = mess.get_sender_id(data)
    if mensaje == "hola":
        mess.send_text_message(sender_id, ["Hola", "¿Cómo estás?"])
    if mensaje == "botones simples":
        botones = b.basic_buttons(["Opción 1", "Opción 2", "🔥"])
        mess.send_button_template(sender_id, "Hola, ¿qué deseas hacer?", botones)
    elif mensaje == "botones complicados":
        cb = b.leave_buttons([{'title': 'Opción 1', 'url': 'https://www.google.com'}, {'title': 'Opción 2', 'call_number': '+525555555555'}])
        mess.send_button_template(sender_id, "Hola, ¿qué deseas hacer?", cb)
    elif mensaje == "imagen":
        r = mess.send_local_attachment(sender_id, 'image', './test.png')
        print(f'\n\n{r}')
    elif mensaje == "ata":
        r = mess.upload_attachment('image', './test.png')
        print(f'\n\n{r}')
    return jsonify({"status": "success"}), 200

if __name__ =='__main__':
    app.run(port=8080, debug=True)