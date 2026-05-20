import requests

for i in range(10):

    response = requests.get("http://127.0.0.1:8000/ask")

    print(i + 1, response.json())