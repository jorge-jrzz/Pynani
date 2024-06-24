from typing import Optional, Union, List, Dict
from .logs import logger


def __make_quick_button(text: Union[str, int], image_url: Optional[str] = None) -> Dict:
    """
    Creates a quick reply button with the specified text, optional image URL, and payload.

    Args:
        text (Union[str, int]): The text or integer to be displayed on the button.
        image_url (Optional[str], optional): The URL of the image to be displayed on the button. Defaults to None.

    Returns:
        Dict: A dictionary representing the quick reply button with its properties.

    Example:
        >>> __make_quick_button("Hello")
        {'content_type': 'text', 'title': 'Hello', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': ''}
        >>> __make_quick_button("World", "https://photos.com/world.jpg")
        {'content_type': 'text', 'title': 'World', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': 'https://photos.com/world.jpg'}
    """

    return {
        "content_type": "text",
        "title": text,
        "payload": "<POSTBACK_PAYLOAD>", 
        "image_url": image_url,
    }

def quick_buttons(buttons: List[Union[str, int]]) -> List[Dict]:
    """
    Prepares a list of quick reply buttons from a list of strings.

    Args:
        buttons (List[Union[str, int]]): A list of strings or integers representing the text for each quick reply button.

    Returns:
        List: A list of dictionaries representing the quick reply buttons with their properties.

    Example:
        >>> quick_buttons(["Hello", "World"])
        [{'content_type': 'text', 'title': 'Hello', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': None}, 
        {'content_type': 'text', 'title': 'World', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': None}]
        >>> quick_buttons([1, 2, 3])
        [{'content_type': 'text', 'title': '1', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': None}, 
        {'content_type': 'text', 'title': '2', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': None}, 
        {'content_type': 'text', 'title': '3', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': None}]
    """

    r_buttons = []
    if len(buttons) > 13:
        logger.warning("Quick replies should be less than 13")
        buttons = buttons[:13]

    for b in buttons:
        r_buttons.append(__make_quick_button(b))

    return r_buttons

def quick_image_buttons(buttons: List[Union[str, int]], images: List[str]) -> List[Dict]:
    """
    Prepares a list of quick reply buttons from a list of strings.

    Args:
        buttons (List[str]): A list of strings or integers representing the text for each quick reply button.
        images (List[str]): A list of strings representing the image URL for each quick reply button.

    Returns:
        List: A list of dictionaries representing the quick reply buttons with their properties.

    Example:
        >>> quick_image_buttons(["Hello", "World"], ["https://photos.com/hello.jpg", "https://photos.com/world.jpg"])
        [{'content_type': 'text', 'title': 'Hello', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': 'https://photos.com/hello.jpg'}, 
        {'content_type': 'text', 'title': 'World', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': 'https://photos.com/world.jpg'}]
    If a button does not have an image, the image URL should be None or an empty string.
        >>> quick_image_buttons(["Hello", "World", "Yes"], ["https://photos.com/hello.jpg", "https://photos.com/world.jpg", None])
    """

    r_buttons = []
    if len(buttons) > 13:
        logger.warning("Quick replies should be less than 13")
        buttons = buttons[:13]

    for b, i in zip(buttons, images):
        r_buttons.append(__make_quick_button(b, i))

    return r_buttons
