def asteroid_locations(field):
  locations = set()
  for row in range(len(field)):
    for col in range(len(field[row])):
      if field[row][col] == '#':
        locations.add(point(row, col))
  return locations

def find_nth_destroyed(asteroids, station, n):
  from collections import defaultdict
  angle_to_asteroids = defaultdict(list)
  for asteroid in asteroids:
    if station != asteroid:
      angle = relative_angle(source=station, dest=asteroid)
      angle_to_asteroids[angle].append(asteroid)
  dist_from_station = lambda p: distance(station, p)
  for angle in angle_to_asteroids:
    angle_to_asteroids[angle] = sorted(angle_to_asteroids[angle], key=dist_from_station)
  sorted_angles = sorted(angle_to_asteroids.keys(), key=lambda angle: -1 * angle)

  last = None
  angle_index = 0
  points_for_angle_index = lambda index: angle_to_asteroids[sorted_angles[angle_index]]
  next_in_ring = lambda index: (index + 1) % len(sorted_angles)
  for i in range(n):
      while angle_index == len(sorted_angles) or len(points_for_angle_index(angle_index)) == 0:
        angle_index = next_in_ring(angle_index)
      last = points_for_angle_index(angle_index).pop(0)
      angle_index = next_in_ring(angle_index)
  return last

def count_visible(asteroids, location):
  angle_set = set()
  for asteroid in asteroids:
    if asteroid != location:
      angle = relative_angle(location, asteroid)
      angle_set.add(angle)
  return len(angle_set)

def distance(a, b):
  x_delta = b[0] - a[0]
  y_delta = b[1] - a[1]
  from math import sqrt
  return sqrt(x_delta ** 2 + y_delta ** 2)

def relative_angle(source, dest):
  (source_x, source_y) = source
  (dest_x, dest_y) = dest
  from math import atan2
  return atan2(dest[1] - source[1], dest[0] - source[0])
  
def point(row, col):
  return (row, col)

def get_input():
  filename = '10.txt'
  return [line.rstrip('\n') for line in open(filename)]

def answer(point):
  (row, col) = point
  return col * 100 + row
  
if __name__ == '__main__':
  field = get_input()
  asteroids = asteroid_locations(field)
  station = max(asteroids, key=lambda station: count_visible(asteroids, station))
  n = 200
  print(answer(find_nth_destroyed(asteroids, station, n)))