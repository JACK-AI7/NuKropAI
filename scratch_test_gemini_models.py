import requests
import json
API_KEY = "AIzaSyCG6qwfNmBSErUu6V6Xs7_tDGeb5NmxPv4"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
response = requests.get(url)
data = response.json()
for model in data.get('models', []):
    name = model.get('name')
    methods = model.get('supportedGenerationMethods', [])
    if 'generateContent' in methods and 'gemini' in name:
        print(name)
