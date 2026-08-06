import requests

url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b&format=json&limit=5&filters[state]=Maharashtra&filters[commodity]=Wheat"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

resp = requests.get(url, headers=headers)
print(resp.status_code)
if resp.status_code == 200:
    data = resp.json()
    print("Total:", data.get('total'))
    print("Records length:", len(data.get('records', [])))
else:
    print(resp.text)
