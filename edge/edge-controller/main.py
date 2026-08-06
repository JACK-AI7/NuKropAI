import os
import time
import json
import paho.mqtt.client as mqtt

# Local & Cloud Config
LOCAL_HOST = os.getenv("LOCAL_MQTT_HOST", "localhost")
CLOUD_HOST = os.getenv("CLOUD_MQTT_HOST", "mqtt.nukrop.io")
FARM_ID = os.getenv("FARM_ID", "default_farm")

# State tracking for offline survivability
cloud_connected = False
pending_telemetry = []

def on_cloud_connect(client, userdata, flags, rc):
    global cloud_connected
    if rc == 0:
        print("✅ Edge connected to NuKropAI Cloud EMQX")
        cloud_connected = True
        # Subscribe to cloud commands meant for this farm
        client.subscribe(f"nukrop/cloud/cmd/farm/{FARM_ID}/#")
        # Flush pending telemetry
        flush_telemetry(client)
    else:
        print("❌ Cloud connection failed")

def on_cloud_disconnect(client, userdata, rc):
    global cloud_connected
    print("⚠️ Cloud disconnected. Entering OFFLINE AUTONOMOUS mode.")
    cloud_connected = False

def on_cloud_message(client, userdata, msg):
    # A cloud AI orchestration event tells the edge to open a valve
    print(f"☁️ Cloud Command Received: {msg.topic} -> {msg.payload.decode()}")
    
    # Forward the command to the LOCAL broker so physical ESP32/Tuya devices actuate
    topic_parts = msg.topic.split('/')
    device_id = topic_parts[-1]
    
    local_topic = f"nukrop/local/cmd/device/{device_id}"
    local_client.publish(local_topic, msg.payload)
    print(f"🔄 Relayed to local edge device: {local_topic}")

def flush_telemetry(client):
    global pending_telemetry
    for t in pending_telemetry:
        client.publish(t['topic'], t['payload'])
    pending_telemetry.clear()

def on_local_message(client, userdata, msg):
    # Local ESP32 node sent telemetry (e.g. soil moisture)
    print(f"📡 Local Telemetry Received: {msg.topic}")
    
    # Process local autonomous rules here (e.g., if moisture < 30%, open valve immediately)
    payload = json.loads(msg.payload.decode())
    if payload.get("moisture", 100) < 30:
        print("🔥 CRITICAL: Local moisture too low! Triggering offline fallback irrigation!")
        local_client.publish(f"nukrop/local/cmd/device/{payload.get('valve_id')}", json.dumps({"action": "OPEN"}))
    
    # Forward telemetry to cloud
    cloud_topic = msg.topic.replace("local", "cloud")
    if cloud_connected:
        cloud_client.publish(cloud_topic, msg.payload)
    else:
        # Buffer to disk/memory
        pending_telemetry.append({"topic": cloud_topic, "payload": msg.payload})

# Setup Cloud Client
cloud_client = mqtt.Client("EdgeNode_" + FARM_ID)
cloud_client.on_connect = on_cloud_connect
cloud_client.on_disconnect = on_cloud_disconnect
cloud_client.on_message = on_cloud_message

# Setup Local Client
local_client = mqtt.Client("EdgeController_Local")
local_client.on_message = on_local_message

if __name__ == "__main__":
    print("🚀 Starting NuKropAI Edge Orchestrator...")
    
    # Connect local
    try:
        local_client.connect(LOCAL_HOST, 1883, 60)
        local_client.subscribe("nukrop/local/telemetry/#")
        local_client.loop_start()
    except Exception as e:
        print(f"Local MQTT Error: {e}")

    # Connect cloud
    try:
        # Note: In production, configure TLS certificates here
        cloud_client.connect(CLOUD_HOST, 1883, 60)
        cloud_client.loop_forever()
    except Exception as e:
        print(f"Cloud MQTT Error: {e}. Running in pure local mode.")
        while True:
            time.sleep(1)
