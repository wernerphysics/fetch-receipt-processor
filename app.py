import uuid
import math
from datetime import date, time
from flask import Flask, request
from validators import ValidationError, validate_receipt

app = Flask(__name__)

# As per the requirements, receipt storage is ephemeral. There is no persistence between sessions.
receipts = {}


@app.post("/receipts/process")
def process_receipt():
    """
    Given a valid receipt in the request body, create a new uuid for that receipt and save it in the
    receipts dict.
    """
    try:
        validate_receipt(request.json)
    except ValidationError as e:
        return {"error": e.message}, 400

    id = str(uuid.uuid4())
    receipts[id] = request.json
    return {"id": id}, 201


@app.route("/receipts/<id>/points")
def get_points(id):
    """
    If a receipt with the given id exists, return its point value according to the following rules:
        1 point for every alphanumeric character in retailer name
        50 points if the total is a round dollar amount with no cents
        25 points if the total is a multiple of 0.25
        5 points for every two items on the receipt
        If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2
            and round up to the nearest integer. The result is the number of points earned.
        6 points if the day in the purchase date is odd
        10 points if the time of purchase is after 2:00PM and before 4:00pm.
    """
    if not id in receipts:
        return "id not found", 404

    receipt = receipts[id]
    retailer = receipt["retailer"]
    purchase_date = receipt["purchaseDate"]
    purchase_time = receipt["purchaseTime"]
    total = float(receipt["total"])
    items = receipt["items"]

    points = 0
    points += sum(1 for c in retailer if c.isalnum())
    if total == round(total):
        points += 50
    if total % 0.25 == 0:
        points += 25
    points += 5 * (len(items) // 2)
    for item in items:
        price = float(item["price"])
        description = item["shortDescription"].strip()
        if len(description) % 3 == 0:
            points += math.ceil(0.2 * price)
    if date.fromisoformat(purchase_date).day % 2 == 1:
        points += 6
    hour = time.fromisoformat(purchase_time).hour
    if hour >= 14 and hour < 16:
        points += 10

    return {"points": points}
