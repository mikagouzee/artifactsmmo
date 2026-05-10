from api_client import api

def get_all_maps(layer, content_type,content_code, hide_blocked_maps=True):
  endpoint = f'/maps?'

  if layer:
    endpoint += f"layer={layer}&"

  if content_type:
    endpoint+= f"content_type={content_type}&"

  if content_code:
    endpoint += f"content_code={content_code}&"
  
  if hide_blocked_maps:
    endpoint += f"hide_blocked_maps={hide_blocked_maps}&"

  return api.request('GET', endpoint)
