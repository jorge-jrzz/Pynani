from typing import Optional, Union


class Buttons:
    def __make_button(self, title: str, url: Optional[str] = None, call_number: Optional[str] = None) -> dict:
        if url is not None and call_number is not None:
            raise ValueError("You can't have both url and call_number at the same time")
        
        if url:
            type_button = "web_url"
            url_button = url
            payload_button = ""
        elif call_number:
            type_button = "phone_number"
            url_button = ""
            payload_button = call_number
        elif not url and not call_number:
            type_button = "postback"
            url_button = ""
            payload_button = "DEVELOPER_DEFINED_PAYLOAD"
        
        return {
            "type": type_button,
            "title": title,
            "payload": payload_button, 
            "url": url_button,
        }
    
    def basic_buttons(self, buttons: Union[str, list]) -> list:
        if isinstance(buttons, str):
            return [self.__make_button(buttons)]
        else:
            if len(buttons) > 3:
                print("Buttons template should be less than 3")
                buttons = buttons[:3]
            return [self.__make_button(button) for button in buttons]
    
    def leave_buttons(self, buttons: Union[dict, list]):
        if isinstance(buttons, dict):
            return [self.__make_button(**buttons)]
        else:
            if len(buttons) > 3:
                print("Buttons template should be less than 3")
                buttons = buttons[:3]
            return [self.__make_button(**button) for button in buttons]

        
# bb = Button()
# # print(bb.basic_buttons(["Hola", "Mundo", "🔥"]))
# print(bb.leave_buttons([{"title": "Hola", "url": "https://www.google.com"}, {"title": "Mundo", "call_number": "+525555555555"}]))


