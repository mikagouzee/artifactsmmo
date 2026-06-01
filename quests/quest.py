class quest:
  type: str
  target: str
  quantity: int
  progress: int
  
  def __init__(self, name:str):
    self.name = name
    

  async def run(self, context, action_controller, db_controller):
    #returns enums.TaskResult
    pass