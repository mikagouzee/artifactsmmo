class quest:
  type: str
  target: str
  
  def __init__(self, name:str):
    self.name = name
    

  async def run(self, context, action_controller, db_controller):
    #returns enums.TaskResult
    pass