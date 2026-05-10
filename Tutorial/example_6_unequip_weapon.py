TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# Unequip the item in the weapon slot — moves it back to your inventory
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/unequip"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

# Specify which slot to unequip (weapon, helmet, boots, ring1, etc.)
body = { "slot": "weapon" }

try:
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    
    if "error" in data:
        raise Exception(data["error"]["message"])
        
    character = data["data"]["character"]
    print(f"🎒 Unequipped weapon! It is now in your inventory.")
    print(f"📦 Inventory capacity: {len(character['inventory'])} / {character['inventory_max_items']}")
except Exception as e:
    print(f"❌ {e}")