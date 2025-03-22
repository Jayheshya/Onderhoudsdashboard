import requests
import json

api_key = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjU4NzE3YzkzOWMwYzQwMTdiN2JmNDgwMjEyNzM3NDY5IiwiaCI6Im11cm11cjEyOCJ9"
url = "https://api.knmi.nl/v1/weather"
parameters = {"location": "Amsterdam", "apikey": api_key}

try:
    response = requests.get(url, params=parameters)
    response.raise_for_status()
    weergegevens = response.json()
except requests.RequestException as e:
    print("Fout bij ophalen weergegevens:", e)
    weergegevens = {}