TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# Craft the wooden staff — requires 4x Ash Wood + 1x Wooden Stick in your inventory
# Make sure you are at the workshop (2,1) before running this!
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/crafting"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# "code" is the item identifier you want to craft
body = { "code": "wooden_staff" }

try:
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    
    if "error" in data:
        raise Exception(data["error"]["message"])
        
    details = data["data"]["details"]
    print(f"🔨 Crafted 1x wooden_staff successfully!")
    print(f"🌟 {details['xp']} Weaponcrafting XP gained.")
except Exception as e:
    print(f"❌ {e}")