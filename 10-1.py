def find_max(field):
  asteroids = asteroid_locations(field)
  return max(count(asteroids, station_location) for station_location in asteroids) - 1

def asteroid_locations(field):
  locations = set()
  for row in range(len(field)):
    for col in range(len(field[row])):
      if field[row][col] == '#':
        locations.add(point(col, row))
  return locations

def count(asteroids, location):
  vectors = set()
  for asteroid in asteroids:
    vector = normalised_vector(source=location, dest=asteroid)
    vectors.add(str(vector))
  return len(vectors)

def normalised_vector(source, dest):
  from fractions import Fraction
  import math
  (source_x, source_y) = source
  (dest_x, dest_y) = dest
  (delta_x, delta_y) = (dest_x - source_x, dest_y - source_y)
  if delta_y == 0:
    ratio = Fraction(0, 1)
  else:
    ratio = Fraction(delta_x, delta_y)
  return (sign(delta_x), sign(delta_y), ratio)

def sign(n):
  if n < 0:
    return -1
  elif n == 0:
    return 0
  else:
    return 1

def point(row, col):
  return (row, col)

def get_input():
  filename = '10.txt'
  return [line.rstrip('\n') for line in open(filename)]
  
if __name__ == '__main__':
  field = get_input()
  print(find_max(field))