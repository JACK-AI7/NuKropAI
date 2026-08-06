import os
import sys
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import time

# Platform Configuration
# Get variables securely from Environment Variables (Set these up in GitHub Secrets)
GOVT_API_KEY = os.environ.get("GOVT_API_KEY", "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b")
DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", "postgresql://postgres:password@db.supabase.co:5432/postgres")

API_ENDPOINT = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
CHUNK_FETCH_LIMIT = 10000 
MAX_RETRIES = 10

def extract_and_load_pipeline():
    print(f"[{datetime.now()}] Initializing live extraction pipeline process...")
    current_offset = 0
    collected_records = []
    
    # Session block handling persistent connections
    session = requests.Session()
    
    consecutive_failures = 0
    
    while True:
        target_url = f"{API_ENDPOINT}?api-key={GOVT_API_KEY}&format=json&limit={CHUNK_FETCH_LIMIT}&offset={current_offset}"
        try:
            print(f"Fetching batch offset block: {current_offset}...")
            response = session.get(target_url, timeout=30)
            
            if response.status_code == 429:
                print(f"WARNING: Rate limited (429). Backing off...")
                consecutive_failures += 1
                time.sleep(min(120, 2 ** consecutive_failures)) # Exponential backoff
                continue
                
            if response.status_code != 200:
                print(f"CRITICAL ERROR: Source server rejected handshakes. Code {response.status_code}")
                consecutive_failures += 1
                if consecutive_failures >= MAX_RETRIES:
                    print("Max retries reached. Breaking extraction loop.")
                    break
                time.sleep(5)
                continue
                
            # Reset failures on success
            consecutive_failures = 0
                
            payload = response.json()
            records_chunk = payload.get("records", [])
            
            if not records_chunk:
                print("Pagination extraction complete. Reached terminal vector block.")
                break
                
            collected_records.extend(records_chunk)
            current_offset += CHUNK_FETCH_LIMIT
            
            # Gentle sleep to respect rate limits
            time.sleep(1)
            
        except Exception as network_exception:
            print(f"Network processing exception encountered: {network_exception}")
            consecutive_failures += 1
            if consecutive_failures >= MAX_RETRIES:
                print("Max retries reached due to network errors. Breaking extraction loop.")
                break
            time.sleep(min(60, 2 ** consecutive_failures))

    if not collected_records:
        print("Data extraction failed or empty array returned. Pipeline execution halted gracefully.")
        return
        
    print(f"Total extracted commodity rows compiled: {len(collected_records)}. Processing transformations...")

    # Data transformation and pipeline execution matrix
    cleaned_insert_payload = []
    for node in collected_records:
        try:
            cleaned_insert_payload.append((
                str(node.get('state', '')).strip().title(),
                str(node.get('district', '')).strip().title(),
                str(node.get('market', '')).strip(),
                str(node.get('commodity', '')).strip(),
                str(node.get('variety', '')).strip(),
                str(node.get('arrival_date', '')).strip(),
                float(node.get('min_price', 0) or 0),
                float(node.get('max_price', 0) or 0),
                float(node.get('modal_price', 0) or 0)
            ))
        except (ValueError, TypeError) as conversion_error:
            continue # Drops damaged numerical cells safely to protect transaction consistency

    if not cleaned_insert_payload:
        print("No valid rows to insert after transformation.")
        return

    # Establish atomic transactional pipeline connection block
    try:
        print("Initializing connection pool block to operational app database...")
        db_connection = psycopg2.connect(DB_CONNECTION_STRING)
        db_cursor = db_connection.cursor()
        
        print("Truncating database state matrix storage metrics cleanly...")
        db_cursor.execute("TRUNCATE TABLE public.mandi_live_rates;")
        
        bulk_insert_query = """
            INSERT INTO public.mandi_live_rates (state, district, market, commodity, variety, arrival_date, min_price, max_price, modal_price)
            VALUES %s;
        """
        
        print("Injecting bulk structured arrays directly via high speed execute_values pattern...")
        execute_values(db_cursor, bulk_insert_query, cleaned_insert_payload)
        
        db_connection.commit()
        print(f"Pipeline executed successfully. Synchronized {len(cleaned_insert_payload)} rows to client availability vectors.")
        
    except Exception as operational_database_error:
        print(f"FAIL: Operational database connection rejected entry executions: {operational_database_error}")
        if 'db_connection' in locals():
            db_connection.rollback()
    finally:
        if 'db_connection' in locals():
            db_cursor.close()
            db_connection.close()

if __name__ == "__main__":
    while True:
        extract_and_load_pipeline()
        print("Sleeping for 4 hours before next complete sync cycle...")
        time.sleep(4 * 60 * 60)
