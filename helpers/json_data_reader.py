import json
from pathlib import Path

def read_json(file_name):
  path = Path(__file__).resolve().parent.parent/"data"/f"{file_name}"
  
  with open(path, 'r') as f:
      asJson = json.load(f)
      return asJson