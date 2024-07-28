import requests
from config import API_KEY, BASE_URL

def fetch_address(search_text):
    url = f"{BASE_URL}?input={search_text}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def process_data(data):
    if data and data['status'] == 'ok' and data['predictions']:
        prediction = data['predictions'][0]
        description = prediction['description']
        location = prediction['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return description, lat, lng
    else:
        return None, None, None