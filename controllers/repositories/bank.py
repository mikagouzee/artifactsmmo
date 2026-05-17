class bank_repository:
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

    
    
    async def get_bank_inventory(self):
        resp = await self._request_wrapper("get", f'/my/bank/items')
        data = resp.json()
        return data["data"]
