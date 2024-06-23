from typing import Optional, List, Any


def get_address(street_1: str, city: str, postal_code: str, state: str, country: str, street_2: Optional[str] = None) -> dict:
    return {
        "street_1": street_1,
        "street_2": street_2,
        "city": city,
        "postal_code": postal_code,
        "state": state,
        "country": country
    }


def get_summary(total_cost: float, subtotal: Optional[float] = None, shipping_cost: Optional[float] = None, total_tax: Optional[float] = None):
    return {
        "subtotal": subtotal,
        "shipping_cost": shipping_cost,
        "total_tax": total_tax,
        "total_cost": total_cost
    }


def get_adjustments(*args: Any) -> list:
    adjustments = []
    for i in range(0, len(args), 2):
        adjustment = {
            "name": args[i],
            "amount": args[i + 1]
        }
        adjustments.append(adjustment)
    return adjustments


def get_elements(title: str, price: float, subtitle: Optional[str] = None, quantity: Optional[int] = None, currency: Optional[str] = 'USD', image_url: Optional[str] = None) -> List[dict]:
    item = {
        "title": title,
        "subtitle": subtitle,
        "quantity": quantity,
        "price": price,
        "currency": currency,
        "image_url": image_url
    }
    return [item]
