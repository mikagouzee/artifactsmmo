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
    # Attempt to extract cooldown info from common places in the error payload
    cd = None
    if isinstance(error_data, dict):
      cd = (error_data.get("cooldown", {}) or {}).get("total_seconds")
      if cd is None:
        cd = (error_data.get("data", {}) or {}).get("cooldown", {}).get("total_seconds")

    # If an explicit cooldown is provided, set the hero's next action time
    if cd:
      try:
        cd_val = float(cd)
        context.next_action_time = time.time() + cd_val
      except Exception:
        pass
    # If error code indicates character in cooldown (499) but no cooldown value,
    # set a small backoff to avoid tight retry loops
    elif error_code == 499:
      context.next_action_time = time.time() + 2

    # Short sleep to yield control and avoid immediate retry storms
    await asyncio.sleep(0.1)
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