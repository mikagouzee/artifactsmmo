TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# Equip the wooden staff from your inventory into the weapon slot
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/equip"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# "code" = item to equip, "slot" = which slot to put it in
body = { "code": "wooden_staff", "slot": "weapon" }

try:
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    
    if "error" in data:
        raise Exception(data["error"]["message"])
        
    char = data["data"]["character"]
    print(f"✅ Equipped wooden_staff in weapon slot!")
    print(f"⚔️  Your earth attack is now {char['earth_attack']}")
except Exception as e:
    print(f"❌ {e}")