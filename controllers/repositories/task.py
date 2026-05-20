from decorators.api_result import api_result


class task_repository:
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
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/task/new')
  
  @api_result
  async def complete_task(self, context):
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/task/complete')
  
  @api_result
  async def task_trade(self, context, quantity):
    payload = {'code': context.current_hero.task, 'quantity': quantity}
    return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/task/trade', json=payload)
    

