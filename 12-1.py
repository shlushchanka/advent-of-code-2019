def iterate(positions, velocites):
  velocites_delta = calculate_velocity_delta(positions)
  for i in range(len(velocites)):
    velocites[i] = sum_tuples(velocites[i], velocites_delta[i])
    positions[i] = sum_tuples(positions[i], velocites[i])

def calculate_velocity_delta(positions):
  n = len(positions)
  velocites = [(0, 0, 0) for i in range(n)]
  for i in range(n):
    for j in range(i + 1, n):
      gravity = gravity_for_position(positions[i], positions[j])
      velocites[i] = sum_tuples(velocites[i], gravity)
      velocites[j] = sum_tuples(velocites[j], negate_gravity(gravity))
  return velocites

def negate_gravity(gravity):
  return tuple([-g for g in gravity])

def sum_tuples(a, b):
  return tuple([sum(t) for t in [t for t in zip(*[a, b])]])

def gravity_for_position(current_position, other_position):
  return tuple([gravity_for_dimension(c, o) for (c, o) in zip(current_position, other_position)])

def gravity_for_dimension(current, other):
  if current < other:
    return 1
  elif current == other:
    return 0
  else:
    return -1;

def get_input():
  filename = '12.txt'
  for line in open(filename):
    line = line.rstrip('\n')  
    
def energy(tuple):
  return sum([abs(t) for t in tuple])

if __name__ == '__main__':
  positions = [
    (-1, -4, 0),
    (4, 7, -1),
    (-14, -10, 9),
    (1, 2, 17)
  ]
  velocities = [(0, 0, 0) for i in range(4)]
  for i in range(1000):
    iterate(positions, velocities)
  print(positions)
  print(velocities)
  tot = sum([energy(positions[i]) * energy(velocities[i]) for i in range(4)])
  print(tot)
