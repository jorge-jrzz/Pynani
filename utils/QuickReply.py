class QuickReply():
    def _quick_button(self, text: str, image_url: str = None, payload: str = "<POSTBACK_PAYLOAD>", content_type: str = "text") -> dict:
        return {
            "content_type": content_type,
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
                r_buttons.append(self._quick_button(b))

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
                r_buttons.append(self._quick_button(**b))

        return r_buttons
    

# qq = QuickReply()
# l = ["1", "2", "3"]
# t = [{"text": "1", "image_url": "https://www.google.com"}, {"text": "2", "image_url": "https://www.google.com"}]
# # print(qq.)
# print("----")
# print(qq.quick_buttons(l))
# print("----")
# print(qq.quick_buttons_image(t))

