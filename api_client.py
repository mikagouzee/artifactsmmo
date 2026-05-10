import os
import json
import requests
import time
from dotenv import load_dotenv


load_dotenv()

with open('config.json', 'r') as f:
    config = json.load(f)

# Configuration globale
CHAR_NAME = config.get('CHARACTER_NAME')
BASE_URL = "https://api.artifactsmmo.com"


class artifacts_client:
  def __init__(self):
     self.session = requests.Session()
     self.session.headers.update({
      "Authorization": f"Bearer {os.getenv('Token')}",
      "Content-Type": "application/json"    
     })


  #TODO : ADD ERROR HANDLING
  def request(self, method, endpoint, data=None):
        url = f"{BASE_URL}{endpoint}"
        
        # Exécution de la requête
        response = self.session.request(method, url, json=data)
        data = response.json()

        if "error" in data:
          # raise Exception(data["error"]["message"])
          print(f"An Error Happened : {data["error"]} : {data["error"]["message"]} .")

        # print(f"res from {endpoint}: {response_data}")
        # La structure de l'API Artifacts place souvent le cooldown dans data['cooldown']
        if "data" in data and "cooldown" in data["data"]:
            seconds = data["data"]["cooldown"]["remaining_seconds"]
            if seconds > 0:
                print(f"[Cooldown] Attente de {seconds}s...")
                time.sleep(seconds+1)

        # if "data" in data and "character" in data["data"]:
            

        return data
  
api = artifacts_client()