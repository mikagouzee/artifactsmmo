from decorators.api_result import api_result


class hero_repository:
  def __init__(self, http_client):
    self.http = http_client
    self.total_api_calls = 0

  async def _request_wrapper(self, method, endpoint, **kwargs):
    """Middleware central pour monitorer et compter chaque appel API"""
    self.total_api_calls += 1
    # print(f"📡 [API CALL #{self.total_api_calls}] {method.upper()} {endpoint} | Args: {kwargs.get('params', kwargs.get('json', ''))}")
    
    if method.lower() == "get":
        return await self.http.get(endpoint, **kwargs)
    elif method.lower() == "post":
        return await self.http.post(endpoint, **kwargs)

  @api_result
  async def craft(self, context, item_code, quantity=1):
    payload = {'code': item_code, 'quantity': quantity}
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/crafting', json=payload)
    
  @api_result
  async def equip(self, context, item_code, slot="weapon", qtty=1):
    payload = {'code': item_code, 'slot': slot, 'quantity': qtty}
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/equip', json=payload)
    
  @api_result
  async def fight(self, context):  
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/fight')

  @api_result
  async def gather(self, context):
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/gathering')
    
  @api_result
  async def move(self, context, x, y):
    payload = {'x': x, 'y': y}
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/move', json=payload)
    
  @api_result
  async def rest(self, context):
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/rest')

  @api_result
  async def use_item(self, context, item_code, qtty=1):
    payload = {"code": item_code, "quantity": qtty}
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/use', json=payload)
   
     