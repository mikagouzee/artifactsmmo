import asyncio
import sys

from CLI.bot_argument_parser import BotArgumentParser
from quests.gather import gather_quest as GatherQuest


class Listener():
  def __init__(self):
    self.parser = None
    self.init_parser()
    
  async def listen(self, gamemaster):
    loop = asyncio.get_event_loop()
    while True:
      # reader = asyncio.StreamReader()
      # await loop.connect_read_pipe(
      #   lambda: asyncio.StreamReaderProtocol(reader), sys.stdin
      # )

      line = await loop.run_in_executor(None, sys.stdin.readline)
      user_input = line.strip()
      if user_input:
        try:
          args = self.parser.parse_args(user_input.split())
          if args.command is None:
            self.parser.print_help()
            continue
          self.handle(args, gamemaster)
        except Exception as e: 
          print(f"Unexpected error : {e}")


  def init_parser(self):

    self.parser = BotArgumentParser(prog="bot")
    subparsers = self.parser.add_subparsers(dest="command")

    # "assign gather --hero Alice --item spruce_wood --quantity 50"
    assign = subparsers.add_parser("assign")
    assign_sub = assign.add_subparsers(dest="quest_type")

   # defines that the later arguments are for gather
    gather = assign_sub.add_parser("gather")
    gather.add_argument("--hero", required=True)
    gather.add_argument("--item", required=True)
    gather.add_argument("--quantity", type=int, default=10)


  def handle(self, args, gamemaster):
    hero_context = next(
      (c for c in gamemaster.hero_contexts if c.current_hero.name == args.hero),
      None
    )
    if not hero_context:
      print(f"hero {args.hero} not found!")
      return
    
    match args.quest_type:
      case "gather":
        quest = GatherQuest(item_code=args.item, quantity=args.quantity)
        hero_context.quest_log.append_back(quest)
        print(f"✔ Assigned gather {args.quantity}x {args.item} to {args.hero}")
      case _:
        print(f"Unknown quest type: {args.quest_type}")