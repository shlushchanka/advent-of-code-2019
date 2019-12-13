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
    
def iterate_single_dimension(positions):
  n = len(positions)
  velocities = [0 for i in range(n)]
  visited = set()
  step = 0
  while True:
    state = str(positions) + str(velocities)
    if state in visited:
      return step
    visited.add(state)
      
    for i in range(n):
      for j in range(i + 1, n):
        gravity = gravity_for_dimension(positions[i], positions[j])
        velocities[i] += gravity
        velocities[j] -= gravity

    for i in range(n):
      positions[i] += velocities[i]

    step += 1
    #print(step)
    
def lcm(a, b):
  from math import gcd
  gcd = gcd(a, b)
  return a * b // gcd

if __name__ == '__main__':
  positions = [
    (-1, -4, 0),
    (4, 7, -1),
    (-14, -10, 9),
    (1, 2, 17)
  ]
  #Example 1
  # positions = [
  #   (-1, 0, 2),
  #   (2, -10, -7),
  #   (4, -8, 8),
  #   (3, 5, -1)
  # ]
  #Example 2
  # positions = [
  #   (-8, -10, 0),
  #   (5, 5, 10),
  #   (2, -7, 3),
  #   (9, -8, -3)
  # ]
  x_positions = [p[0] for p in positions]
  y_positions = [p[1] for p in positions]
  z_positions = [p[2] for p in positions]
  x = iterate_single_dimension(x_positions)
  y = iterate_single_dimension(y_positions)
  z = iterate_single_dimension(z_positions)
  print(lcm(x, lcm(y, z)))

  
  
