from decorators.api_result import api_result
from helpers import check_bag_weight, check_quantity_in_bag


class bank_repository:
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
    async def deposit(self, context, item_code=None, quantity=None):
        
        endpoint = f'/my/{context.current_hero.name}/action/bank/deposit/item'
        
        if item_code is None:
            payload = [{"code": i["code"], "quantity": i["quantity"]} for i in context.current_hero.inventory if i.get("quantity", 0) > 0]
            return await self._request_wrapper("post", endpoint, json=payload)
        elif quantity and quantity > 0:
                payload = [{'code': item_code, 'quantity': quantity or 1}]
                return await self._request_wrapper("post", endpoint, json=payload)
        else: 
            quantity = check_quantity_in_bag(context.current_hero.inventory, item_code)
            payload = [{'code': item_code, 'quantity': quantity}]
            return await self._request_wrapper("post", endpoint, json=payload)

    @api_result
    async def deposit_all_but(self, context, item_list):
        
        endpoint = f'/my/{context.current_hero.name}/action/bank/deposit/item'
        payload = [{"code": i["code"], "quantity": i["quantity"]} for i in context.current_hero.inventory if i.get("quantity", 0) > 0 and i["code"] not in item_list]
        return await self._request_wrapper("post", endpoint, json=payload)
        
    @api_result
    async def deposit_gold(self, context):
       
        
        endpoint = f'/my/{context.current_hero.name}/action/bank/deposit/gold'
    
        payload = {"quantity": context.current_hero.gold}
            
        return await self._request_wrapper("post", endpoint, json=payload)
        
    @api_result
    async def withdraw(self, context, item_code, quantity=1):
        
        payload = [{'code': item_code, 'quantity': quantity}]
        return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/bank/withdraw/item', json=payload)
    
    @api_result
    async def withdraw_items(self, context, items_list: list):
        """
        Withdraw multiple items from the bank.
        
        Args:
            context: The hero withdrawing items
            items_list: List of dicts with 'code' and 'quantity' keys
                    e.g., [{"code": "copper_bar", "quantity": 5}, {"code": "raw_chicken", "quantity": 10}]
        """
        
        payload = [{'code': item['code'], 'quantity': item.get("quantity", 1)} for item in items_list]
        return await self._request_wrapper("post", f'/my/{context.current_hero.name}/action/bank/withdraw/item', json=payload)
        
    #direct method, no context, just data
    async def get_bank_inventory(self):
        """Returns an array of code/quantity/slot, but not the full item!"""
        all_items = []
        page = 1
        while True:
            resp = await self._request_wrapper("get", f'/my/bank/items', params={"page": page})
            data = resp.json()
            all_items.extend(data["data"])
            if page >= data["pages"]:
                break
            page += 1
        return all_items
