TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# Move to tile (-1, 0) where the Ash Tree is located
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/move"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# Target coordinates: the Ash Tree resource node
body = { "x": -1, "y": 0 }

try:
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    
    if "error" in data:
        raise Exception(data["error"]["message"])
        
    destination = data["data"]["destination"]
    cooldown = data["data"]["cooldown"]
    
    print(f"✅ Moved to ({destination['x']}, {destination['y']}) on {destination['name']}")
    print(f"⏳ Wait {cooldown['total_seconds']}s before gathering!")
except Exception as e:
    print(f"❌ {e}")