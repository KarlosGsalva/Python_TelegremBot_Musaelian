import requests
import os

from dotenv import load_dotenv

load_dotenv()

NGROK_URL = os.getenv("NGROK_URL")
user_id = 6594296991


def test_accessibility_api():
    response = requests.get(f"{NGROK_URL}api")
    assert response.status_code == 200


def test_accessibility_export_json():
    response = requests.get(f"{NGROK_URL}export/json/?id={user_id}")
    assert response.status_code == 200


def test_accessibility_export_csv():
    response = requests.get(f"{NGROK_URL}export/csv/?id={user_id}")
    assert response.status_code == 200
