
def closest_coordinates(a, b):
  return abs(a[0] -b[0]) + abs(a[1] - b[1])

def check_location(hero, x, y):
  if hero.x == x and hero.y == y:
    return True
  return False
