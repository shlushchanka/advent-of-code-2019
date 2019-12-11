from IntCodeComputer import IntCodeComputer

def get_input():
  return [3,8,1005,8,311,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,29,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,50,1,2,19,10,1006,0,23,1,103,14,10,1,1106,15,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,88,1006,0,59,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,113,2,101,12,10,2,1001,0,10,2,1006,14,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,146,1,1106,11,10,1006,0,2,1,9,8,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,180,1,6,13,10,1,1102,15,10,2,7,1,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1002,8,1,213,1006,0,74,2,1005,9,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,243,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,264,2,104,8,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,290,101,1,9,9,1007,9,952,10,1005,10,15,99,109,633,104,0,104,1,21101,387512640296,0,1,21101,0,328,0,1106,0,432,21102,1,665749660564,1,21101,339,0,0,1106,0,432,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,179318226984,1,1,21101,386,0,0,1105,1,432,21101,46266346499,0,1,21101,0,397,0,1105,1,432,3,10,104,0,104,0,3,10,104,0,104,0,21102,709580555028,1,1,21102,420,1,0,1106,0,432,21102,1,988220642068,1,21101,0,431,0,1106,0,432,99,109,2,21202,-1,1,1,21101,40,0,2,21102,1,463,3,21102,1,453,0,1106,0,496,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,458,459,474,4,0,1001,458,1,458,108,4,458,10,1006,10,490,1102,0,1,458,109,-2,2105,1,0,0,109,4,2102,1,-1,495,1207,-3,0,10,1006,10,513,21101,0,0,-3,21201,-3,0,1,22101,0,-2,2,21102,1,1,3,21101,532,0,0,1106,0,537,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,560,2207,-4,-2,10,1006,10,560,22102,1,-4,-4,1105,1,628,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,1,579,0,1105,1,537,22101,0,1,-4,21101,1,0,-1,2207,-4,-2,10,1006,10,598,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,620,22101,0,-1,1,21102,620,1,0,106,0,495,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0]

class Robot:
  def __init__(self):
    self.row = 0
    self.col = 0
    self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    self.direction_index = 0

  def rotate_clockwise(self):
    self.rotate_delta(1)

  def rotate_counter_clockwise(self):
    self.rotate_delta(-1)

  def rotate_delta(self, delta):
    self.direction_index = (len(self.directions) + self.direction_index + delta) %  len(self.directions)

  def move(self):
    (row_delta, col_delta) = self.directions[self.direction_index]
    self.row += row_delta
    self.col += col_delta

  @property
  def position(self):
    return (self.row, self.col)

def filled_coordinates(program):
  COLOR_BLACK = 0
  COLOR_WHITE = 1
  robot_computer = IntCodeComputer(program, std_in=[], std_out=[])
  robot = Robot()
  from collections import defaultdict
  panel_color = defaultdict(lambda: COLOR_BLACK, {(0, 0): COLOR_WHITE})
  while not robot_computer.is_halted:
    robot_computer.std_in.append(panel_color[robot.position])
    robot_computer.run()
    panel_color[robot.position] = robot_computer.std_out.pop(0)
    if robot_computer.std_out.pop(0) == 0:
      robot.rotate_counter_clockwise()
    else:
      robot.rotate_clockwise()
    robot.move()

  filled_coordinates = [p for p in panel_color if panel_color[p] == COLOR_WHITE]
  return filled_coordinates

def render_image(filled_coordinates):
  import numpy as np
  import matplotlib.pyplot as plt
  
  (xs_min, xs_max) = min_and_max(filled_coordinates, first)
  (ys_min, ys_max) = min_and_max(filled_coordinates, second)
  image = np.zeros((xs_max - xs_min + 1, ys_max - ys_min + 1))

  for (x, y) in filled_coordinates:
    image[x - xs_min, y - ys_min] = 1

  plt.imshow(image)
  plt.show()

def first(tuple):
  return tuple[0]

def second(tuple):
  return tuple[1]

def min_and_max(items, key):
  return (min_element(items, key), max_element(items, key))

def min_element(items, key):
  return find_key(items, min, key)

def max_element(items, key):
  return find_key(items, max, key)

def find_key(items, find_function, key):
  item = find_function(items, key=key)
  return key(item)
  
if __name__ == '__main__':
  program = get_input()
  image = filled_coordinates(program)
  render_image(image)