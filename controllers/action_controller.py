import asyncio
from dataclasses import replace
from models import hero

class ActionController:
  def __init__(self, http_client):
    self.http = http_client
    self.http.base_url = "https://api.artifactsmmo.com"
    self._maps_cache = []
    self.total_api_calls = 0 
  
  async def get_all_heroes(self): 
    
    resp = await self._request_wrapper("get", '/my/characters')
    data = resp.json()
    return [hero(**char) for char in data["data"]]

  async def _request_wrapper(self, method, endpoint, **kwargs):
    """Middleware central pour monitorer et compter chaque appel API"""
    self.total_api_calls += 1
    # print(f"📡 [API CALL #{self.total_api_calls}] {method.upper()} {endpoint} | Args: {kwargs.get('params', kwargs.get('json', ''))}")
    
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

  async def craft(self, context, item_code, quantity=1):
    await self._limiter()
    payload = {'code': item_code, 'quantity': quantity}
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/crafting', json=payload)
    return await self.process_result(resp.json(), context)

  async def deposit(self, context, item_code=None, quantity=None):
    await self._limiter()
    endpoint = f'/my/{context.current_hero.name}/action/bank/deposit/item'
    if item_code is None:
        payload = [{"code": i["code"], "quantity": i["quantity"]} for i in context.inventory if i.get("quantity", 0) > 0]
        if not payload: return context
    else:
        payload = [{'code': item_code, 'quantity': quantity or 1}]
    
    resp = await self._request_wrapper("post", endpoint, json=payload)
    return await self.process_result(resp.json(), context)

  async def deposit_gold(self, context):
    await self._limiter()
    endpoint = f'/my/{context.current_hero.name}/action/bank/deposit/gold'
  
    payload = {"quantity": context.gold}
        
    resp = await self._request_wrapper("post", endpoint, json=payload)
    return await self.process_result(resp.json(), context)

  async def equip(self, context, item_code, slot="weapon", qtty=1):
    await self._limiter()
    payload = {'code': item_code, 'slot': slot, 'quantity': qtty}
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/equip', json=payload)
    return await self.process_result(resp.json(), context)

  async def fight(self, context):
    await self._limiter()
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/fight')
    return await self.process_result(resp.json(), context)

  async def gather(self, context):
    await self._limiter()
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/gathering')
    return await self.process_result(resp.json(), context)

  async def move(self, context, x, y):
    await self._limiter()
    payload = {'x': x, 'y': y}
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/move', json=payload)
    return await self.process_result(resp.json(), context)

  async def rest(self, context):
    await self._limiter()
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/rest')
    return await self.process_result(resp.json(), context)

  async def use_item(self, context, item_code, qtty=1):
    await self._limiter()
    payload = {"code": item_code, "quantity": qtty}
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/use', json=payload)
    return await self.process_result(resp.json(), context)
  
  async def withdraw(self, context, item_code, quantity=1):
    await self._limiter()
    payload = [{'code': item_code, 'quantity': quantity}]
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/bank/withdraw/item', json=payload)
    return await self.process_result(resp.json(), context)

  async def withdraw_items(self, context, items_list: list):
    """
    Withdraw multiple items from the bank.
    
    Args:
        context: The hero withdrawing items
        items_list: List of dicts with 'code' and 'quantity' keys
                   e.g., [{"code": "copper_bar", "quantity": 5}, {"code": "raw_chicken", "quantity": 10}]
    """
    await self._limiter()
    payload = [{'code': item['code'], 'quantity': item.get("quantity", 1)} for item in items_list]
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/bank/withdraw/item', json=payload)
    return await self.process_result(resp.json(), context)

  
 
  async def accept_new_task(self, context):
    #   adds the following on the character:
    #   "task": "mushmush",
    #   "task_type": "monsters",
    #   "task_progress": 0,
    #   "task_total": 305,
    # or
    #   "task": "gudgeon",
    #   "task_type": "items",
    #   "task_progress": 0,
    #   "task_total": 306,
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/task/new')
    return await self.process_result(resp.json(), context)
  
  async def complete_task(self, context):
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/task/complete')
    return await self.process_result(resp.json(), context)

  
  async def task_trade(self, context, item_code, quantity):
    payload = {'code': item_code, 'quantity': quantity}
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/task/trade', json=payload)
    return await self.process_result(resp.json(), context)

     
  async def get_bank_inventory(self):
    await self._limiter()
    resp = await self._request_wrapper("get", f'/my/bank/items')
    data = resp.json()
    return data["data"]
