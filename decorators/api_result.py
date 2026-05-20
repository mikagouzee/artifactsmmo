import functools
import asyncio
from dataclasses import replace
import time

def api_result(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        # 'args[0]' est généralement 'self' (le repo)
        context = kwargs.get('context') or args[1]
        response = await func(*args, **kwargs)

        # Extraction propre du JSON ici
        if hasattr(response, 'json'):
            # Si c'est un objet réponse (httpx/requests)
            try:
                json_data = response.json()
            except:
                json_data = {}
        else:
            json_data = response

        # 3. Si le JSON est vide (ex: 204 No Content), on renvoie le contexte tel quel
        if not json_data:
            return context
        # Appel de ton ancienne logique de traitement
        return await process_result(json_data, context)
    
    return wrapper

async def process_result(response, context):
  if "error" in response:
      error_data = response.get("error", {})
      error_code = error_data.get("code")
      message = error_data.get("message")
    # print(f"[{context.current_hero.name}] API Error {error_code}: {message}")
      #error 499: cooldown, just wait longer
      
      #error 497 = inventory full, send hero to deposit stuff

      # FUITE FIX: Si erreur, on force un sleep pour éviter le spam en boucle infinie
      await asyncio.sleep(1)
      return context

  data = response.get("data", {})
  cd = data.get("cooldown", {}).get("total_seconds", 0)
  if cd > 0:
    # await asyncio.sleep(cd + 0.5) # Marge de sécurité
     context.next_action_time = time.time() + cd

  res_char = data.get("character")
  if not res_char and "fight" in data:
    res_char = [char for char in data["characters"] if char.get("name") == context.current_hero.name][0]

  if res_char:  
    context.current_hero = replace(context.current_hero, **res_char)

  return context

# class HeroRepository:
#     @api_result
#     async def move(self, context, x, y):
#         return await self.http.post("/move", json={"x": x, "y": y})