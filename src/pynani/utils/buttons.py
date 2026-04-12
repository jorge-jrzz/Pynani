from typing import Optional, Union, List, Dict
from .logs import get_logger


logger = get_logger(__name__)

def __make_button( title: str, url: Optional[str] = None, call_number: Optional[str] = None) -> Dict:
    """
    Creates a button with the specified title and optional URL or call number.

    Args:
        title (str): The title of the button.
        url (Optional[str], optional): The URL associated with the button. Defaults to None.
        call_number (Optional[str], optional): The call number associated with the button. Defaults to None.

    Returns:
        Dict: A dictionary representing the button with its properties.
    
    Raises:
        ValueError: If both URL and call number are provided.
    
    Example:
        >>> __make_button("Hola", "https://www.google.com")
        {'type': 'web_url', 'title': 'Hola', 'payload': '', 'url': 'https://www.google.com'}
        >>> __make_button("Mundo", call_number="+525555555555")
        {'type': 'phone_number', 'title': 'Mundo', 'payload': '+525555555555', 'url': ''}
        >>> __make_button("Hello")
        {'type': 'postback', 'title': 'Hello', 'payload': 'DEVELOPER_DEFINED_PAYLOAD', 'url': ''}
    """

    if url is not None and call_number is not None:
        logger.error("You can't have both url and call_number at the same time")
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

def basic_buttons( buttons: Union[str, List[Union[str, int]]]) -> List:
    """
    Creates a list of basic buttons.

    Args:
        buttons (Union[str, List[Union[str, int]]]): The buttons to be created. It can be a string or a list of strings or integers.

    Returns:
        List: A list of dictionaries representing the basic buttons with their properties.

    Example:
        >>> basic_buttons(["Hello", "World", "🔥"])
        [{'type': 'postback', 'title': 'Hello', 'payload': 'DEVELOPER_DEFINED_PAYLOAD', 'url': ''}, 
        {'type': 'postback', 'title': 'World', 'payload': 'DEVELOPER_DEFINED_PAYLOAD', 'url': ''}, 
        {'type': 'postback', 'title': '🔥', 'payload': 'DEVELOPER_DEFINED_PAYLOAD', 'url': ''}]
        >>> basic_buttons("Hello")
        [{'type': 'postback', 'title': 'Hello', 'payload': 'DEVELOPER_DEFINED_PAYLOAD', 'url': ''}]
    """

    if isinstance(buttons, str):
        return [__make_button(buttons)]
    else:
        if len(buttons) > 3:
            logger.warning("Buttons template should be less than 3")
            buttons = buttons[:3]
        return [__make_button(button) for button in buttons]

def exit_buttons( buttons: Union[Dict, List[Dict]]) -> List:
    """
    Creates a list of leave buttons.

    Args:
        buttons (Union[Dict, List[Dict]]): The buttons to be created. It can be a dictionary or a list of dictionaries.

    Returns:
        List: A list of dictionaries representing the leave buttons with their properties.
    
    Example:
        >>> leave_buttons([{"title": "Hello", "url": "https://www.google.com"}, {"title": "World", "call_number": "+525555555555"}])
        [{'type': 'web_url', 'title': 'Hello', 'payload': '', 'url': 'https://www.google.com'}, 
        {'type': 'phone_number', 'title': 'World', 'payload': '+525555555555', 'url': ''}]
        >>> leave_buttons({"title": "Hello", "url": "https://www.google.com"})
        [{'type': 'web_url', 'title': 'Hello', 'payload': '', 'url': 'https://www.google.com'}]
    """

    if isinstance(buttons, dict):
        return [__make_button(**buttons)]
    else:
        if len(buttons) > 3:
            logger.warning("Buttons template should be less than 3")
            buttons = buttons[:3]
        return [__make_button(**button) for button in buttons]
