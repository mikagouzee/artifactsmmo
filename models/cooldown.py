from dataclasses import dataclass
@dataclass
class Cooldown:
  total_seconds: int
  remaining_seconds: int
  started_at: str
  expiration: str
  reason: set
    