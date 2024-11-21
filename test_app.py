import uuid
from app import app, receipts

# should be 28 points
target = {
    "retailer": "Target",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {
            "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
            "price": "12.00",
        },
    ],
    "total": "35.35",
}

# should be 109 points
corner_market = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
        {"shortDescription": "Gatorade", "price": "2.25"},
    ],
    "total": "9.00",
}


def test_process_receipt():
    """
    when a receipt is posted to /receipts/process
    then a receipt is created
        and the response includes a new id
        and the id is a valid uuid
    """
    with app.test_client() as client:
        response = client.post("/receipts/process", json=target)

        assert response.status_code == 201, response.json
        assert "id" in response.json
        id = response.json["id"]
        assert id in receipts
        assert is_valid_uuid(id)


def test_points():
    """
    when a receipt is posted to /receipts/process
        and a request is made to /receipts/<id>/points with its id
    then the response includes a points value
        and it's correct for the given payload
    """
    with app.test_client() as client:
        response = client.post("/receipts/process", json=target)
        assert response.status_code == 201, response.json
        id = response.json["id"]
        response = client.get(f"/receipts/{id}/points")
        assert response.json == {"points": 28}

        response = client.post("/receipts/process", json=corner_market)
        assert response.status_code == 201, response.json
        id = response.json["id"]
        response = client.get(f"/receipts/{id}/points")
        assert response.json == {"points": 109}


def test_missing_id():
    """
    given a certain id does not exist in receipts
    when a request is made to /receipts/<id>/points
    then the response is 404
    """
    id = uuid.uuid4()
    with app.test_client() as client:
        response = client.get(f"/receipts/{id}/points")

        assert response.status_code == 404


def is_valid_uuid(id):
    try:
        uuid.UUID(id)
        return True
    except ValueError:
        return False
