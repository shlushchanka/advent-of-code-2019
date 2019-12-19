def get_input():
  filename = '18.txt'
  board = []
  for line in open(filename): 
    line = line.rstrip('\n')  
    row = [c for c in line]
    board.append(row)
  return board

def keys_empty():
  return 0

def keys_key_mask(key):
  index = ord(key) - ord('a')
  return 1 << index

def keys_add(keys, key):
  return keys | keys_key_mask(key)

def keys_contain(keys, key):
  return (keys & keys_key_mask(key)) != 0

def keys_are_full(keys):
  return keys == (1 << 26) - 1

def keys_to_list(keys):
  chars = [chr(ord('a') + i) for i in range(26)]
  return list(filter(lambda c: keys_contain(keys, c), chars))

def find(board, symbol):
  positions = []
  for r in range(len(board)):
    for c in range(len(board[r])):
      if board[r][c] == symbol:
        positions.append((r, c))
  return positions

def neighbors(row, col):
  return [
    (row - 1, col),
    (row, col + 1),
    (row + 1, col), 
    (row, col - 1)
  ]

def is_wall(char):
  return char == '#'

def is_key(char):
  return 'a' <= char <= 'z'

def is_door(char):
  return 'A' <= char <= 'Z'

def key_for_door(char):
  return char.lower()
 
def bfs(board, initial_position, keys_reachable):
  import math
  from collections import deque
  intial_state = (initial_position[0], initial_position[1], keys_empty())
  distance = { intial_state: 0 }
  q = deque([intial_state])
  while len(q) > 0:
    current_state = q.popleft()
    (current_row, current_col, current_keys) = current_state
    current_distance = distance[current_state]
    for (row, col) in neighbors(current_row, current_col):
      char = board[row][col]
      if is_wall(char) or (is_door(char) and not keys_contain(current_keys, key_for_door(char)) and keys_contain(keys_reachable, key_for_door(char))):
        continue
      move_keys = keys_add(current_keys, char) if is_key(char) else current_keys
      move_state = (row, col, move_keys)
      if move_state in distance:
        continue
      move_distance = current_distance + 1
      if move_keys == keys_reachable:
        return move_distance
      distance[move_state] = move_distance
      q.append(move_state)
  return None

def find_reachable_keys(board, initial_position):
  from collections import deque
  visited = set()
  q = deque([initial_position])
  keys = keys_empty()
  while len(q) > 0:
    current_state = q.popleft()
    (current_row, current_col) = current_state
    for neighbor_position in neighbors(current_row, current_col):
      (row, col) = neighbor_position
      char = board[row][col]
      if neighbor_position in visited or is_wall(char):
        continue
      if is_key(char):
        keys = keys_add(keys, char)
      q.append(neighbor_position)
      visited.add(neighbor_position)
  return keys

def replace_one_robot_with_four(board):
  initial_position = find(board, '@')[0]
  (r, c) = initial_position
  board[r - 1][c - 1] = board[r - 1][c + 1] = board[r + 1][c - 1] = board[r + 1][c + 1] = '@'
  board[r][c] = board[r - 1][c] = board[r][c - 1] = board[r][c + 1] = board[r + 1][c] = '#'
  return find(board, '@')

if __name__ == '__main__':
  board = get_input()
  robot_positions = replace_one_robot_with_four(board)
  distances = [bfs(board, p, find_reachable_keys(board, p)) for p in robot_positions]
  print(sum(distances))
  


