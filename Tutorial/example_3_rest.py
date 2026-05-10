TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# API endpoint to make your character rest and recover HP
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/rest"
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
        
    hp_restored = data["data"]["hp_restored"]
    character = data["data"]["character"]
    
    print(f"🛏️  Rested and restored {hp_restored} HP.")
    print(f"❤️  Current HP: {character['hp']}/{character['max_hp']}")
except Exception as e:
    print(f"❌ {e}")