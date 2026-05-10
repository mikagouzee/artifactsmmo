TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# API endpoint for the move action
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/move"

# Authentication headers — your token identifies you on the server
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# Target coordinates: move to tile (0, 1) where the chicken is
body = { "x": 0, "y": 1 }

try:
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    
    if "error" in data:
        raise Exception(data["error"]["message"])
        
    destination = data["data"]["destination"]
    cooldown = data["data"]["cooldown"]
    
    print(f"✅ Moved to ({destination['x']}, {destination['y']}) on {destination['name']}")
    print(f"⏳ Cooldown started: {cooldown['total_seconds']} seconds")
except Exception as e:
    print(f"❌ {e}")