class QuickReply():
    def __make_quick_button(self, text: str, payload: str = "<POSTBACK_PAYLOAD>", image_url: str = None) -> dict:
        return {
            "content_type": "text",
            "title": text,
            "payload": payload, 
            "image_url": image_url if image_url else "",
        }
    
    def quick_buttons(self, buttons: list) -> list:
        r_buttons = []
        if len(buttons) > 13:
            print("Quick replies should be less than 13")
            buttons = buttons[:13]

        for b in buttons:
            if not isinstance(b, str):
                raise ValueError("Each button should be a string")
            else:
                r_buttons.append(self.__make_quick_button(b))

        return r_buttons
    
    def quick_buttons_image(self, buttons: list) -> list:
        r_buttons = []
        if len(buttons) > 13:
            print("Quick replies should be less than 13")
            buttons = buttons[:13]
        for b in buttons:
            if not isinstance(b, dict):
                raise ValueError("Each button should be a dictionary")
            else:
                r_buttons.append(self.__make_quick_button(**b))

        return r_buttons
    

# botones = ['pedro', 'juan', 'popo']
# b_imagen = [{"text": "1", "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b9/Solid_red.png"}, 
#        {"text": "2", "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b9/Solid_red.png"}]
# sb = qui.quick_buttons(botones)
# cb = qui.quick_buttons_image(b_imagen)
