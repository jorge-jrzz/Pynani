from typing import Optional, Union, List, Dict


def get_address(street_1: str, city: str, postal_code: str, state: str, 
                country: str, street_2: Optional[str] = None) -> Dict:
    """
    Constructs an address dictionary from the provided parameters.

    Args:
        street_1 (str): The first line of the street address.
        city (str): The city of the address.
        postal_code (str): The postal code of the address.
        state (str): The state or province of the address.
        country (str): The country of the address.
        street_2 (Optional[str], optional): The second line of the street address. Defaults to None.

    Returns:
        Dict: A dictionary representing the address with its components.

    Example:
        >>> get_address("123 Main St", "Springfield", "12345", "IL", "US", "Apt 1")
        {'street_1': '123 Main St', 'street_2': "Apt 1", 'city': 'Springfield', 'postal_code': '12345', 'state': 'IL', 'country': 'US'}
    Optional parameters can be omitted:
        >>> get_address("123 Main St", "Springfield", "12345", "IL", "US")
        {'street_1': '123 Main St', 'street_2': None, 'city': 'Springfield', 'postal_code': '12345', 'state': 'IL', 'country': 'US'}
    """

    return {
        "street_1": street_1,
        "street_2": street_2,
        "city": city,
        "postal_code": postal_code,
        "state": state,
        "country": country
    }


def get_summary(total_cost: float, subtotal: Optional[float] = None, 
                shipping_cost: Optional[float] = None, total_tax: Optional[float] = None) -> Dict:
    """
    Constructs a summary dictionary from the provided parameters.

    Args:
        total_cost (float): The total cost of the order.
        subtotal (Optional[float], optional): The subtotal of the order. Defaults to None.
        shipping_cost (Optional[float], optional): The shipping cost of the order. Defaults to None.
        total_tax (Optional[float], optional): The total tax of the order. Defaults to None.

    Returns:
        Dict: A dictionary representing the summary with its components.
    
    Example:
        >>> get_summary(100.0, 90.0, 5.0, 5.0)
        {'subtotal': 90.0, 'shipping_cost': 5.0, 'total_tax': 5.0, 'total_cost': 100.0}
    Optional parameters can be omitted:
        >>> get_summary(100.0)
        {'subtotal': None, 'shipping_cost': None, 'total_tax': None, 'total_cost': 100.0}
    """

    return {
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "total_tax": total_tax,
        "total_cost": total_cost
    }


def get_adjustments(*args: Union[str, int, float]) -> List[Dict]:
    """
    Constructs a list of adjustments from the provided arguments.

    Args:
        *args (Union[str, int, float]): A variable number of arguments, where each pair represents an adjustment name and amount.

    Returns:
        List[Dict]: A list of dictionaries, each representing an adjustment with its name and amount.

    Example:
        >>> get_adjustments("Discount", 10, "Tax", 20, "Shipping", 30)
        [{'name': 'Discount', 'amount': 10}, {'name': 'Tax', 'amount': 20}, {'name': 'Shipping', 'amount': 30}]
    """

    adjustments = []
    for i in range(0, len(args), 2):
        adjustment = {
            "name": args[i],
            "amount": args[i + 1]
        }
        adjustments.append(adjustment)
    return adjustments


def get_elements(title: str, price: float, subtitle: Optional[str] = None, 
                 quantity: Optional[int] = None, currency: Optional[str] = 'USD', 
                 image_url: Optional[str] = None) -> List[Dict]:
    """
    Constructs a list of elements from the provided parameters.

    Args:
        title (str): The title of the item.
        price (float): The price of the item.
        subtitle (Optional[str], optional): The subtitle of the item. Defaults to None.
        quantity (Optional[int], optional): The quantity of the item. Defaults to None.
        currency (Optional[str], optional): The currency of the item. Defaults to 'USD'.
        image_url (Optional[str], optional): The URL of the item's image. Defaults to None.

    Returns:
        List: A list of dictionaries representing the elements with their titles, prices, subtitles, quantities, currencies, and image URLs.

    Example:
        >>> get_elements("T-Shirt", 20.0, "Blue", 2, "USD", "https://example.com/tshirt.jpg")
        [{'title': 'T-Shirt', 'subtitle': 'Blue', 'quantity': 2, 'price': 20.0, 'currency': 'USD', 'image_url': 'https://example.com/tshirt.jpg'}]
    Optional parameters can be omitted:
        >>> get_elements("T-Shirt", 20.0)
        [{'title': 'T-Shirt', 'subtitle': None, 'quantity': None, 'price': 20.0, 'currency': 'USD', 'image_url': None}]
    """

    item = {
        "title": title,
        "subtitle": subtitle,
        "quantity": quantity,
        "price": price,
        "currency": currency,
        "image_url": image_url
    }
    return [item]
