def get_input():
  filename = '18.txt'
  lines = []
  for line in open(filename):
    line = line.rstrip('\n')  
    lines.append(line)
  return lines

class Board:
  def __init__(self, board):
    self.board = board
    self.row_count = len(board)
    self.col_count = len(board[0])

  def get(self, row, col):
    return self.board[row][col]

  def boxHasSymbol(self, row, col, symbol):
    return self.get(row, col) == symbol

  def isFree(self, row, col):
    return self.boxHasSymbol(row, col, '.') or self.boxHasSymbol(row, col, '@')

  def isKey(self, row, col):
    return 'a' <= self.get(row, col) <= 'z'

  def isDoor(self, row, col):
    return 'A' <= self.get(row, col) <= 'Z'

  def keyForDoor(self, door):
    return door.lower()

  def canBeMovedTo(self, row, col, keys): 
    return (self.isDoor(row, col) and self.keyForDoor(self.get(row, col)) in keys) or self.isFree(row, col) or self.isKey(row, col)

def find(board, symbol):
  for r in range(len(board)):
    for c in range(len(board[r])):
      if board[r][c] == symbol:
        return (r, c)

def count_keys(board):
  count = 0
  for r in range(len(board)):
    for c in range(len(board[r])):
      if 'a' <= board[r][c] <= 'z':
        count += 1
  return count

def state(position, keys):
  return (position, keys)

def dijkstra(board, initial_position, key_count):
  import math
  from collections import deque
  intial_state = (initial_position, set())
  distance = { str(intial_state): 0 }
  q = deque([intial_state])
  directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
  answer = math.inf
  while len(q) > 0:
    state = q.popleft()
    ((row, col), keys) = state
    if len(keys) == key_count:
      answer = min(answer, distance[str(state)])
    for (delta_row, delta_col) in directions:
      (next_row, next_col) = (row + delta_row, col + delta_col)
      if not board.canBeMovedTo(next_row, next_col, keys):
        continue
      next_keys = set(keys)
      if board.isKey(next_row, next_col):
        next_keys.add(board.get(next_row, next_col))
      next_state = ((next_row, next_col), next_keys)
      next_distance = distance[str(state)] + 1
      if str(next_state) in distance and distance[str(next_state)] <= next_distance:
        continue
      distance[str(next_state)] = next_distance
      q.append(next_state)
  return answer

if __name__ == '__main__':
  input = get_input()
  initial_position = find(input, '@')
  board = Board(input)
  print(dijkstra(board, initial_position, key_count=count_keys(input)))


