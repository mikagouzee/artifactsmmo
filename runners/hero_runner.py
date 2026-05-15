import asyncio


class hero_runner:
  def __init__(self) -> None:
    pass

  async def run(my_hero, inbox: asyncio.PriorityQueue, default_task):
    while True:
      try:
        priority, _, task = inbox.get_nowait()
      except asyncio.QueueEmpty:
        task = default_task

      if task is STOP:
        return
      
      result = await task.run(my_hero)
      #handle result

  class Priority(IntEnum):
    URGENT = 0
    HIGH = 1
    NORMAL = 2
    IDLE = 3