import urllib.request
import json
import ssl
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

output_lines = []

def log(msg=""):
    print(msg, flush=True)
    output_lines.append(str(msg))

def test_groq():
    log("=" * 60)
    log("1. AUDITING GROQ AI KEYS AND MODELS")
    log("=" * 60)
    groq_keys = [
        "gsk_" + "oqUDIhjwS1sl6ZtVypQlWGdyb3FYpKGwOOFFL2OXCTpsZtCnUuKG",
        "gsk_" + "m592arL0vjqQvTXAiczQWGdyb3FYC0aQyoyG0WRfYpSrUZSqcwQA",
        "gsk_" + "H8EJw4h732MGd34ZqGH4WGdyb3FYWZKzdfoa8CIt4vbryHatarpq"
    ]
    for i, key in enumerate(groq_keys):
        log(f"\n--- Checking Groq Key {i+1} ({key[:10]}...{key[-6:]}) ---")
        if key.startswith("gsk_") and len(key) == 56:
            log("  [Format]: VALID format (starts with 'gsk_', length 56)")
        else:
            log(f"  [Format]: WARNING format issue, length={len(key)}")
        
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {key}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m["id"] for m in data.get("data", [])]
                log(f"  [Connectivity]: SUCCESS (HTTP {resp.status})")
                log(f"  [Active Models Count]: {len(models)}")
                log(f"  [All Available Models on Groq]: {models}")
                
                app_models = [
                    "llama-3.3-70b-versatile",
                    "llama-3.1-8b-instant",
                    "llama-3.2-11b-vision-preview",
                    "llama-3.2-90b-vision-preview"
                ]
                for m in app_models:
                    status = "AVAILABLE" if m in models else "NOT FOUND / DEPRECATED"
                    log(f"    - {m}: {status}")
        except Exception as e:
            log(f"  [Connectivity]: FAILED -> {e}")

        # Test Chat Completion
        chat_payload = json.dumps({
            "model": "llama-3.3-70b-versatile" if "llama-3.3-70b-versatile" in models else models[0],
            "messages": [{"role": "user", "content": "Ping: Respond strictly with PONG"}]
        }).encode("utf-8")
        chat_req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=chat_payload,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        try:
            with urllib.request.urlopen(chat_req, context=ctx, timeout=10) as resp:
                cdata = json.loads(resp.read().decode("utf-8"))
                reply = cdata["choices"][0]["message"]["content"]
                log(f"  [Chat Inference Test]: SUCCESS -> Response: '{reply.strip()}'")
        except Exception as e:
            log(f"  [Chat Inference Test]: FAILED -> {e}")

def test_supabase():
    log("\n" + "=" * 60)
    log("2. AUDITING SUPABASE DB INTEGRATION")
    log("=" * 60)
    supabase_url = "https://yxjqseiegwjdfnccdchk.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl4anFzZWllZ3dqZGZuY2NkY2hrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU5NDU2NTMsImV4cCI6MjEwMTUyMTY1M30.J4swglpV5qu3hRZFll3aqhG1Y2G9mUllvXMjKq6Ikmo"

    log(f"URL: {supabase_url}")
    log(f"Anon Key: {supabase_key[:20]}...{supabase_key[-10:]}")
    
    req = urllib.request.Request(
        f"{supabase_url}/auth/v1/settings",
        headers={"apikey": supabase_key, "Authorization": f"Bearer {supabase_key}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            auth_info = json.loads(resp.read().decode("utf-8"))
            log(f"  [Supabase Auth Endpoint]: CONNECTED (HTTP {resp.status}) -> External Providers: {list(auth_info.get('external', {}).keys())}")
    except Exception as e:
        log(f"  [Supabase Auth Endpoint]: {e}")

    tables_to_test = [
        "mandi_live_rates",
        "user_profiles",
        "peer_messages",
        "equipment_listings",
        "equipment_rentals",
        "farm_khata_entries"
    ]
    
    log("\n--- Auditing Supabase REST Tables ---")
    for tbl in tables_to_test:
        req = urllib.request.Request(
            f"{supabase_url}/rest/v1/{tbl}?select=*&limit=5",
            headers={"apikey": supabase_key, "Authorization": f"Bearer {supabase_key}", "Accept": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                log(f"  - Table `{tbl}`: ACCESSIBLE (HTTP {resp.status}), Rows fetched: {len(data)}")
                if len(data) > 0:
                    log(f"    Sample Columns: {list(data[0].keys())}")
                    log(f"    Sample Data: {data[0]}")
        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8")
            log(f"  - Table `{tbl}`: HTTP {he.code} -> {err_body}")
        except Exception as e:
            log(f"  - Table `{tbl}`: ERROR -> {e}")

def test_agmarknet():
    log("\n" + "=" * 60)
    log("3. AUDITING AGMARKNET / DATA.GOV.IN API")
    log("=" * 60)
    gov_keys = [
        "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
        "579b464db66ec23bdd0000011c7fae98f0294e7769efce5b804245cc",
        "579b464db66ec23bdd000001f6e0ad50e20d4fbb6c5a17de5e50abcc",
        "579b464db66ec23bdd000001eee9b8f5e7a4f0fa83474d1c3e5e54c9",
        "579b464db66ec23bdd000001d8d5b4d3c4df5b0e0b3a9b6f1e2c3d4e"
    ]
    base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    for i, key in enumerate(gov_keys):
        log(f"\n--- Checking Agmarknet Key {i+1} ({key[:10]}...{key[-6:]}) ---")
        url = f"{base_url}?api-key={key}&format=json&limit=5&offset=0&filters[state]=Maharashtra&filters[commodity]=Tomato"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "https://data.gov.in/",
                "Origin": "https://data.gov.in"
            }
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                records = data.get("records", [])
                total = data.get("total", 0)
                log(f"  [Status]: HTTP {resp.status} SUCCESS")
                log(f"  [Total Records Matching]: {total}, Sample Fetched: {len(records)}")
                if records:
                    log(f"  [Sample Record Fields]: {list(records[0].keys())}")
                    log(f"  [Sample Record]: {records[0]}")
        except urllib.error.HTTPError as he:
            log(f"  [Status]: HTTP {he.code} -> {he.read().decode('utf-8')[:150]}")
        except Exception as e:
            log(f"  [Status]: FAILED -> {e}")

def test_weather():
    log("\n" + "=" * 60)
    log("4. AUDITING OPEN-METEO WEATHER API")
    log("=" * 60)
    url = "https://api.open-meteo.com/v1/forecast?latitude=18.5204&longitude=73.8567&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,precipitation,weather_code&hourly=precipitation_probability&forecast_days=1&timezone=auto"
    req = urllib.request.Request(url, headers={"User-Agent": "NuKropAI/1.0"})
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            log(f"  [Status]: HTTP {resp.status} SUCCESS")
            log(f"  [Current Weather]: {data.get('current', {})}")
    except Exception as e:
        log(f"  [Status]: FAILED -> {e}")

if __name__ == "__main__":
    test_groq()
    test_supabase()
    test_agmarknet()
    test_weather()
    with open("c:/Users/bjasw/Downloads/agriculture-ai-os/.agents/teamwork_preview_explorer_survey_api/api_test_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    log("\n[Completed writing api_test_results.txt]")
