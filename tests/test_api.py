import random
import re
import uuid

import requests

BASE_URL = "https://qa-internship.avito.com/api/1"
UUID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)

def generate_seller_id():
    return random.randint(111111, 999999)


def extract_item_id(response_json):
    status_text = response_json.get("status", "")
    match = UUID_PATTERN.search(status_text)
    assert match, f"Could not extract item UUID from response: {response_json}"
    return match.group(0)


def create_item(seller_id):
    payload = {
        "sellerId": seller_id,
        "name": "Test Item",
        "price": 1000,
        "statistics": {
            "likes": 1,
            "viewCount": 10,
            "contacts": 2
        }
    }
    response = requests.post(f"{BASE_URL}/item", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    return extract_item_id(response_json), payload


def test_create_item():
    seller_id = generate_seller_id()
    item_id, payload = create_item(seller_id)

    assert str(uuid.UUID(item_id)) == item_id


def test_get_item_by_id():
    seller_id = generate_seller_id()
    item_id, payload = create_item(seller_id)

    response = requests.get(f"{BASE_URL}/item/{item_id}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list) and len(data) == 1
    item = data[0]
    assert item["name"] == payload["name"]
    assert item["price"] == payload["price"]


def test_get_items_by_seller():
    seller_id = generate_seller_id()
    item_id_1, _ = create_item(seller_id)
    item_id_2, _ = create_item(seller_id)

    response = requests.get(f"{BASE_URL}/{seller_id}/item")
    assert response.status_code == 200

    items = response.json()
    item_ids = {item["id"] for item in items}
    assert item_id_1 in item_ids
    assert item_id_2 in item_ids


def test_get_statistics():
    seller_id = generate_seller_id()
    item_id, payload = create_item(seller_id)

    response = requests.get(f"{BASE_URL}/statistic/{item_id}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list) and len(data) == 1
    stats = data[0]
    assert stats["likes"] == payload["statistics"]["likes"]


def test_get_nonexistent_item():
    nonexistent_item_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/item/{nonexistent_item_id}")
    assert response.status_code == 404
