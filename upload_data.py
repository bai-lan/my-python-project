import requests
import json

url = "http://localhost:5000/red-wines/upload"

payload = json.dumps([
  {
    "name": "Wine E",
    "year": 2024,
    "region": "Region E",
    "price": 25,
    "fixed_acidity": 7.2,
    "volatile_acidity": 0.8
  }
])
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
print(response.status_code)
print(response)
