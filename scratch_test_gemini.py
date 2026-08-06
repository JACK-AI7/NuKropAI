import requests

API_KEYS = [
    "AIzaSyCG6qwfNmBSErUu6V6Xs7_tDGeb5NmxPv4",
    "AIzaSyBE7bk1FwVJGRomLsBinLI7RMIwcHmOrH0"
]
MODELS = [
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash"
]

for model in MODELS:
    for key in API_KEYS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": "Hello, are you there?"}]
                }
            ]
        }
        resp = requests.post(url, json=payload)
        print(f"Model: {model}, Key ending in {key[-4:]} -> Status: {resp.status_code}")
        if resp.status_code != 200:
            print("Error details:", resp.text)
