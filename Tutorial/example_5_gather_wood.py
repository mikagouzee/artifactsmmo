TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# Gather the resource on the current tile (Ash Tree at -1,0)
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/gathering"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

try:
    response = requests.post(url, headers=headers)
    data = response.json()
    
    if "error" in data:
        raise Exception(data["error"]["message"])
        
    details = data["data"]["details"]
    drops_str = ", ".join([f"{i['quantity']}x {i['code']}" for i in details["items"]])
    
    print(f"🪓 Gathered successfully! Gained: {drops_str}")
    print(f"🌟 {details['xp']} Woodcutting XP gained.")
except Exception as e:
    print(f"❌ {e}")