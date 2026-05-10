import asyncio
from dataclasses import replace
from helpers import closest_coordinates
from models import hero, world_map

class ActionController:
  def __init__(self, http_client):
    self.http = http_client
    self.http.base_url = "https://api.artifactsmmo.com"
    self._maps_cache = []
    self.total_api_calls = 0  # Compteur local
  
  async def load_world_map(self):
    """À appeler une seule fois au lancement du main"""
    if self._maps_cache:
        return
        
    print("Chargement de la carte du monde en mémoire...")
    page = 1
    while True:
        # On utilise directement le client http pour éviter de passer par get_all_maps
        response = await self.http.get("/maps", params={"page": page, "size": 100})
        data = response.json()
        self._maps_cache.extend(data["data"])
        
        if page >= (data["total"] // 100) + 1:
            break
        page += 1
    print(f"{len(self._maps_cache)} maps chargées en cache.")

  async def _limiter(self):
    # Un petit délai de sécurité minimum pour forcer 
    # une latence humaine et éviter le spamming CPU
    await asyncio.sleep(0.5)

  async def _request_wrapper(self, method, endpoint, **kwargs):
        """Middleware interne pour monitorer les appels"""
        self.total_api_calls += 1
        print(f"📡 [API CALL #{self.total_api_calls}] {method.upper()} {endpoint} | Args: {kwargs.get('params', kwargs.get('json', ''))}")
        
        # Appel réel
        if method == "get":
            return await self.http.get(endpoint, **kwargs)
        elif method == "post":
            return await self.http.post(endpoint, **kwargs)

  async def process_result(self, response, aHero):
    if "error" in response:
        try:
            error_data = response.get("error", {})
            error_code = error_data.get("code")
            message = error_data.get("message")
            
            print(f"[{aHero.name}] API Error {error_code}: {message}")

            # Cas spécifique : Monstre non présent ou perso déplacé (mort)
            if error_code == 498: # Exemple: Character not at location
                 print(f"[{aHero.name}] Character lost or dead. Syncing position...")
                 # On ne fait rien de spécial, le replace() plus bas mettra à jour la position
        except Exception:
            print(f"[{aHero.name}] Critical Error: {error_data if error_data else 'NA'} -- {message if message else 'NA'}")
            return aHero

    data = response.get("data", {})

    cd = data.get("cooldown", {}).get("total_seconds", 0)
    if cd > 0:
      await asyncio.sleep(cd + 1)

    if "fight" in data:
      res_char = [char for char in data["characters"] if char.get("name") == aHero.name][0]
    else:
      res_char = data.get("character")

    if res_char:  
      aHero = replace(aHero, **res_char)

    return aHero

  async def craft(self, aHero, item_code, quantity=1):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/crafting'
    payload = {'code':item_code, 'quantity':quantity}

    data = await self.http.post(endpoint, json=payload)
    data = data.json()
    return await self.process_result(data, aHero)

  async def deposit(self, aHero, item_code=None, quantity=None):
    await self._limiter()
    endpoint = f'/my/{aHero.name}/action/bank/deposit/item'
    
    # CAS 1 : On dépose tout l'inventaire
    if item_code is None:
        if not aHero.inventory:
            return aHero    

        # Si tes objets sont des dataclasses, utilise item.code
        # Si ce sont des dicts (comme dans ton dump), utilise item["code"]
        payload = [
            {"code": item["code"], "quantity": item["quantity"]} 
            for item in aHero.inventory 
            if item.get("code") and item.get("quantity", 0) > 0
        ]
        
        if not payload:
            return aHero

    # CAS 2 : On dépose un item spécifique
    else:
        if quantity is not None and quantity < 1:
            raise Exception(f"deposit value cannot be lower than 1 : {quantity}")
        
        payload = [{'code': item_code, 'quantity': quantity or 1}]

    # On envoie le payload (soit le bulk, soit l'unique)
    data = await self.http.post(endpoint, json=payload)
    return await self.process_result(data.json(), aHero)

  async def equip(self, aHero, item_code, slot="weapon", qtty=1):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/equip'

    payload = {
      'code':item_code,
      'slot':slot,
      'quantity':qtty}

    data = await self.http.post(endpoint, json=payload)
    data = data.json()

    return await self.process_result(data, aHero)

  async def fight(self, aHero):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/fight'
    data = await self.http.post(endpoint)
    data = data.json()

    return await self.process_result(data, aHero)

  async def gather(self, aHero):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/gathering'
    data = await self.http.post(endpoint)
    data = data.json()
    return await self.process_result(data, aHero)

  async def get_all_maps(self,params=None):
    
    endpoint =f'/maps?'

    response = await self._request_wrapper("get", "/maps", params=params)
    return response.json()

  async def get_all_heroes(self):
    await self._limiter()
    endpoint =f'/my/characters'
    data = await self.http.get(endpoint)
    data = data.json()

    return [hero(**char) for char in data["data"]] #should be an array of heroes
      
  async def get_closest_map(self, hero, content_type=None, content_code=None, hide_blocked_maps=True):
    if not self._maps_cache:
       await self.load_world_map()

    print(f'Looking for closest map : {content_type} - {content_code}')

    filtered_maps = []

    for m in self._maps_cache:
      interactions = m.get("interactions", {})
      content = interactions.get("content") if interactions else None
      if not content:
         continue
      
      match_type = not content_type or content.get("type") == content_type
      match_code = not content_code or content.get("code") == content_code

      if match_type and match_code:
        filtered_maps.append(m)

    if not filtered_maps:
        return None
    
    # 2. On trouve la plus proche (ta logique actuelle)
    start = (hero.x, hero.y)
    shortest = float('inf')
    destination = None
    
    for val in filtered_maps:
        map_obj = world_map(**val)
        crt = closest_coordinates(start, (map_obj.x, map_obj.y))
        if crt < shortest:
            destination = map_obj
            shortest = crt

    return destination
  
  async def move(self, aHero, x, y):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/move'
    payload = {'x':x, 'y':y}
    
    data = await self.http.post(endpoint, json=payload)
    data = data.json()
    return await self.process_result(data, aHero)

  async def rest(self, aHero):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/rest'
    data = await self.http.post(endpoint)
    data = data.json()
    return await self.process_result(data, aHero)

  async def use_item(self, aHero, item_code, qtty=1):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/use'
    payload = {  "code": item_code, "quantity": qtty }
    data = await self.http.post(endpoint, json=payload)
    data = data.json()
    return await self.process_result(data, aHero)
  
  async def withdraw(self, aHero, item_code, quantity=1):
    await self._limiter()
    endpoint =f'/my/{aHero.name}/action/bank/withdraw/item'
    payload = [{'code':item_code, 'quantity':quantity}]
    data = await self.http.post(endpoint, json=payload)
    data = data.json()
    return await self.process_result(data, aHero)