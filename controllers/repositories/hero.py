class hero_repository:
  def __init__(self, http_client):
    self.http = http_client


  async def _request_wrapper(self, method, endpoint, **kwargs):
    """Middleware central pour monitorer et compter chaque appel API"""
    self.total_api_calls += 1
    # print(f"📡 [API CALL #{self.total_api_calls}] {method.upper()} {endpoint} | Args: {kwargs.get('params', kwargs.get('json', ''))}")
    
    if method.lower() == "get":
        return await self.http.get(endpoint, **kwargs)
    elif method.lower() == "post":
        return await self.http.post(endpoint, **kwargs)

  async def craft(self, context, item_code, quantity=1):
    await self._limiter()
    payload = {'code': item_code, 'quantity': quantity}
    resp = await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/crafting', json=payload)
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
   
     