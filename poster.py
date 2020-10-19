import requests
import json

with open('mail.json') as json_file:
    data = json.load(json_file)

r = requests.post("http://localhost:8080", json={'json_payload': data})