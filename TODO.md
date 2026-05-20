Step 1 — argparse basics (30min)
Build a throwaway parser.py that parses a hardcoded string. No game, no async, just learn the API. Get comfortable with add_subparsers, add_argument, parse_args.
Step 2 — wire argparse to a string instead of sys.argv (15min)
By default argparse reads sys.argv. You'll learn to pass your own list instead:
pythonparser.parse_args(["assign", "gather", "--hero", "Alice", "--item", "spruce_wood"])
That's literally the only difference from a normal CLI.
Step 3 — write the cli_listener coroutine (20min)
The async stdin reader from above. For now just print() whatever it receives, no parsing yet.
Step 4 — plug argparse into the listener (20min)
Connect Step 2 into Step 3. Parse the line, print back what was understood. Still no game logic touched.
Step 5 — act on game_runner (30min)
Find the right hero_context by name, append the right quest to its quest_log.
Step 6 — handle bad input gracefully (15min)
argparse likes to sys.exit() on errors — you'll need to catch that so a typo doesn't kill your bot.