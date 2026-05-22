import asyncio
from dataclasses import replace
from controllers.repositories.bank import bank_repository
from controllers.repositories.hero import hero_repository
from controllers.repositories.task import task_repository
from models import hero

class ActionController:
  def __init__(self, http_client):
    self.http = http_client
    self.http.base_url = "https://api.artifactsmmo.com"
    self._maps_cache = []
    self.total_api_calls = 0 
    self.bank = bank_repository(http_client)
    self.task = task_repository(http_client)
    self.hero = hero_repository(http_client)
  
  async def get_all_heroes(self): 
    
    resp = await self._request_wrapper("get", '/my/characters')
    data = resp.json()
    return [hero(**char) for char in data["data"]]

  async def _request_wrapper(self, method, endpoint, **kwargs):
    """Middleware central pour monitorer et compter chaque appel API"""
    self.total_api_calls += 1
    
    if method.lower() == "get":
        return await self.http.get(endpoint, **kwargs)
    elif method.lower() == "post":
        return await self.http.post(endpoint, **kwargs)

  async def _limiter(self):
    await asyncio.sleep(0.5)

  async def process_result(self, response, context):
    if "error" in response:
        error_data = response.get("error", {})
        error_code = error_data.get("code")
        message = error_data.get("message")
        print(f"[{context.current_hero.name}] API Error {error_code}: {message}")
        
        #error 497 = inventory full, send hero to deposit stuff

        # FUITE FIX: Si erreur, on force un sleep pour éviter le spam en boucle infinie
        await asyncio.sleep(1)
        return context

    data = response.get("data", {})
    cd = data.get("cooldown", {}).get("total_seconds", 0)
    if cd > 0:
      await asyncio.sleep(cd + 0.5) # Marge de sécurité

    res_char = data.get("character")
    if not res_char and "fight" in data:
      res_char = [char for char in data["characters"] if char.get("name") == context.current_hero.name][0]

    if res_char:  
      context = replace(context.current_hero, **res_char)
    return context

  