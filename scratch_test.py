import requests

API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key={API_KEY}&format=json&limit=10&filters[state]=Maharashtra&filters[commodity]=Tomato"

response = requests.get(url)
print(response.status_code)
print(response.json())
