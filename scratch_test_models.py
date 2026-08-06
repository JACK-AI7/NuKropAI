import requests
API_KEY = "AIzaSyCG6qwfNmBSErUu6V6Xs7_tDGeb5NmxPv4"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
response = requests.get(url)
print(response.status_code)
print(response.text)
