import argparse

class BotArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            print(message)
        # do nothing instead of sys.exit()

    def error(self, message):
        print(f"❌ Command error: {message}")
        self.print_help()