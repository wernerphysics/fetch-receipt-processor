import re
from datetime import date, time


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


def validate_receipt(receipt):
    for field in ("retailer", "purchaseDate", "purchaseTime", "items", "total"):
        if field not in receipt:
            raise ValidationError(f"receipt is missing required field '{field}'")

    if not re.match("^[\\w\\s\\-&]+$", receipt["retailer"]):
        raise ValidationError(
            f"retailer '{receipt["retailer"]}' has invalid characters."
        )

    try:
        date.fromisoformat(receipt["purchaseDate"])
    except ValueError:
        raise ValidationError(
            f"purchase date '{receipt['purchaseDate']}' isn't a valid ISO date string."
        )

    try:
        time.fromisoformat(receipt["purchaseTime"])
    except ValueError:
        raise ValidationError(
            f"purchase time '{receipt['purchaseTime']}' isn't a valid ISO time string."
        )

    if len(receipt["items"]) == 0:
        raise ValidationError("The receipt must contain at least one item.")

    for item in receipt["items"]:
        validate_item(item)

    if not re.match("^\\d+\\.\\d{2}$", receipt["total"]):
        raise ValidationError(
            f"receipt total '{receipt['total']}' isn't a valid price string."
        )


def validate_item(item):
    for field in ("shortDescription", "price"):
        if field not in item:
            raise ValidationError(f"receipt item is missing required field: {field}")

    if not re.match("^[\\w\\s\\-]+$", item["shortDescription"]):
        raise ValidationError(
            f"item description '{item['shortDescription']}' has invalid characters."
        )

    if not re.match("^\\d+\\.\\d{2}$", item["price"]):
        raise ValidationError(
            f"item price '{item["price"]}' isn't a valid price string."
        )
