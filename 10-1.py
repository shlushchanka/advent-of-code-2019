def asteroid_locations(field):
  locations = set()
  for row in range(len(field)):
    for col in range(len(field[row])):
      if field[row][col] == '#':
        locations.add(point(col, row))
  return locations

def count_visible(asteroids, location):
  angle_set = set()
  for asteroid in asteroids:
    if asteroid != location:
      angle = relative_angle(location, asteroid)
      angle_set.add(angle)
  return len(angle_set)

def relative_angle(source, dest):
  (x, y) = vector(source, dest)
  from math import atan2
  return atan2(y, x)

def vector(source, dest):
  return tuple([d - s for (s, d) in zip(source, dest)])

def point(x, y):
  return (x, y)

def get_input():
  filename = '10.txt'
  return [line.rstrip('\n') for line in open(filename)]
  
if __name__ == '__main__':
  field = get_input()
  asteroids = asteroid_locations(field)
  print(max(count_visible(asteroids, station_location) for station_location in asteroids))