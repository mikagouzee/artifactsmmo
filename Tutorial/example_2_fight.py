TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Im1pY2hlbC5nb3V6ZWVAaG90bWFpbC5jb20iLCJwYXNzd29yZF9jaGFuZ2VkIjpudWxsfQ.mNCPw4hQKSQ2TxNxRPLQTHFT-VHWkP3XMq1UYt_vTzk"
CHARACTER_NAME = "Semet"

import requests

# API endpoint to start a fight against the monster on the current tile
url = f"https://api.artifactsmmo.com/my/{CHARACTER_NAME}/action/fight"
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
        
    fight = data["data"]["fight"]
    fight_stats = fight["characters"][0]
    
    print("🏆 Fight won!" if fight["result"] == "win" else "💀 Fight lost!")
    print(f"⚔️  XP gained: {fight_stats['xp']} | HP remaining: {fight_stats['final_hp']}")
    
    if len(fight_stats["drops"]) > 0:
        drops_str = ", ".join([f"{d['quantity']}x {d['code']}" for d in fight_stats["drops"]])
        print(f"🎁 Loot dropped: {drops_str}")
except Exception as e:
    print(f"❌ {e}")