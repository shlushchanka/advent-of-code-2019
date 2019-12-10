def find_max(field):
  asteroids = asteroid_locations(field)
  return max(count(asteroids, station_location) for station_location in asteroids)

def asteroid_locations(field):
  locations = set()
  for row in range(len(field)):
    for col in range(len(field[row])):
      if field[row][col] == '#':
        locations.add(point(row, col))
  return locations

def count(asteroids, location):
  from collections import defaultdict
  angles = defaultdict(list)
  for asteroid in asteroids:
    if location != asteroid:
      angle = relative_angle(source=location, dest=asteroid)
      angles[angle].append(asteroid)
  for angle in angles:
    angles[angle] = sorted(angles[angle], key=lambda p: dist(p, location))
  sorted_angles = sorted(angles.keys(), key=lambda angle: -1 * angle)
  cpy = []
  order = {}
  i = 0
  while i < 200:
    for angle in sorted_angles:
      if len(angles[angle]) == 0:
        continue
      cpy.append(angles[angle].pop(0))
      i += 1
  if len(angles) == 263:
    print(cpy[199][1] * 100 + cpy[199][0])
  return len(angles)

def dist(a, b):
  x_delta = b[0] - a[0]
  y_delta = b[1] - a[1]
  from math import sqrt
  return sqrt(x_delta ** 2 + y_delta ** 2)

def relative_angle(source, dest):
  (source_x, source_y) = source
  (dest_x, dest_y) = dest
  from math import atan2
  return atan2(dest[1] - source[1], dest[0] - source[0])
  

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