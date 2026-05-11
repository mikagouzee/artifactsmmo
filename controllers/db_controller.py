from models.beanies.map_tile import MapTile


class DbController:
  def __init__(self, http_client):
    self.http = http_client
    self.http.base_url = "https://api.artifactsmmo.com"
    self._maps_cache = []
    self.total_api_calls = 0 

  async def _request_wrapper(self, method, endpoint, **kwargs):
    """Middleware central pour monitorer et compter chaque appel API"""
    self.total_api_calls += 1
    print(f"📡 [API CALL #{self.total_api_calls}] {method.upper()} {endpoint} | Args: {kwargs.get('params', kwargs.get('json', ''))}")
  
    if method.lower() == "get":
        return await self.http.get(endpoint, **kwargs)
    elif method.lower() == "post":
        return await self.http.post(endpoint, **kwargs)

  async def load_world_map(self):
    if self._maps_cache:
        return
        
    print("Chargement de la carte du monde en mémoire...")
    page = 1
    while True:
        # Utilisation du wrapper pour le chargement initial aussi
        response = await self._request_wrapper("get", "/maps", params={"page": page, "size": 100})
        data = response.json()
        self._maps_cache.extend(data["data"])
        
        if page >= (data["total"] // 100) + 1:
            break
        page += 1
    print(f"{len(self._maps_cache)} maps chargées en cache.")

  async def sync_world_map(self):
    page = 1
    total_pages = 1
    
    while page <= total_pages:
        response = await self._request_wrapper("get", "/maps", page=page) # Ta méthode API existante
        data = response.get("data", [])
        total_pages = response.get("pages", 1)

        for tile_data in data:
            # Extraction propre des interactions
            content = None
            if tile_data.get("interactions") and tile_data["interactions"].get("content"):
                content = MapContent(**tile_data["interactions"]["content"])
            
            # Upsert : On cherche par map_id, si trouvé on met à jour, sinon on crée
            tile = MapTile(
                map_id=tile_data["map_id"],
                name=tile_data["name"],
                x=tile_data["x"],
                y=tile_data["y"],
                layer=tile_data["layer"],
                skin=tile_data["skin"],
                content=content,
                blocked=(tile_data["access"]["type"] == "blocked")
            )
            
            await MapTile.find_one(MapTile.map_id == tile.map_id).upsert(
                {"$set": tile.dict(exclude={'id'})}, 
                on_insert=tile
            )
        
        print(f"Page {page}/{total_pages} synchronisée...")
        page += 1

  async def get_closest_map_v2(self, hero, entity_code:str):
    targets = await MapTile.find(MapTile.content.code == entity_code).to_list()
    if not targets: 
        return None
    
    closest = min(
        targets, 
        key=lambda t: abs(t.x - hero.x) + abs(t.y - hero.y)
    )    
    return closest

  async def sync_resources(self):
    response = await self.http_client.get("/resources")
    data = response.json()
    resources_data = data.get("data", [])

    for res_dict in resources_data:
        existing = await Resource.find_one(Resource.code == res_dict["code"])
        if existing:
            await existing.update({"$set": res_dict})
        else:
            new_res = Resource(**res_dict)
            await new_res.insert()
            
    print(f"✅ {len(resources_data)} ressources synchronisées en base.")