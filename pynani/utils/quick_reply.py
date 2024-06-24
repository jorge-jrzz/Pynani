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
        [{'content_type': 'text', 'title': 'Hello', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': ''}, 
        {'content_type': 'text', 'title': 'World', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': ''}]
        >>> quick_buttons([1, 2, 3])
        [{'content_type': 'text', 'title': '1', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': ''}, 
        {'content_type': 'text', 'title': '2', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': ''}, 
        {'content_type': 'text', 'title': '3', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': ''}]
    """

    r_buttons = []
    if len(buttons) > 13:
        logger.warning("Quick replies should be less than 13")
        buttons = buttons[:13]

    for b in buttons:
        r_buttons.append(__make_quick_button(b))

    return r_buttons

def quick_buttons_image(buttons: List) -> List[Dict]:
    """
    Prepares a list of quick reply buttons with images from a list of dictionaries.

    Args:
        buttons (List): A list of dictionaries representing the quick reply buttons with their properties.

    Returns:
        List: A list of dictionaries representing the quick reply buttons with their properties, including images.

    Raises:
        ValueError: If each button is not a dictionary.

    Example:
        >>> quick_buttons_image([{"text": "Hello", "image_url": "https://photos.com/hello.jpg"}, {"text": "World", "image_url": "https://photos.com/world.jpg"}])
        [{'content_type': 'text', 'title': 'Hello', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': 'https://photos.com/hello.jpg'}, 
        {'content_type': 'text', 'title': 'World', 'payload': '<POSTBACK_PAYLOAD>', 'image_url': 'https://photos.com/world.jpg'}]
    """

    r_buttons = []
    if len(buttons) > 13:
        logger.warning("Quick replies should be less than 13")
        buttons = buttons[:13]
    for b in buttons:
        if not isinstance(b, dict):
            logger.error("Each button should be a dictionary")
            raise ValueError("Each button should be a dictionary")
        else:
            r_buttons.append(__make_quick_button(**b))

    return r_buttons
