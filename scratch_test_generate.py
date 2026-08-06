import requests

API_KEY = "AIzaSyCG6qwfNmBSErUu6V6Xs7_tDGeb5NmxPv4"
model = "gemini-2.5-flash"

url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
payload = {
    "contents": [
        {
            "parts": [{"text": "Hello, test."}]
        }
    ]
}
resp = requests.post(url, json=payload)
print(resp.status_code)
if resp.status_code != 200:
    print(resp.text)
