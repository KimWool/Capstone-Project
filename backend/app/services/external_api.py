import requests
from typing import Dict, Any

REGISTRY_API_BASE_URL = "https://api.registry.example.com"
BUILDING_API_BASE_URL = "https://api.building.example.com"
API_KEY = "your_api_key_here"

def fetch_registry_data(address: str) -> Dict[str, Any]:
    endpoint = f"{REGISTRY_API_BASE_URL}/getRegistry"
    params = {
        "address": address,
        "api_key": API_KEY
    }
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching registry data: {e}")
        return {}

def fetch_building_data(address: str) -> Dict[str, Any]:
    endpoint = f"{BUILDING_API_BASE_URL}/getBuilding"
    params = {
        "address": address,
        "api_key": API_KEY
    }
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching building data: {e}")
        return {}
