def get_input():
  filename = '18.txt'
  lines = []
  for line in open(filename): 
    line = line.rstrip('\n')  
    lines.append(line)
  return lines

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

def find(board, symbol):
  for r in range(len(board)):
    for c in range(len(board[r])):
      if board[r][c] == symbol:
        return (r, c)

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
 
def bfs(board, initial_position):
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
      if is_wall(char) or (is_door(char) and not keys_contain(current_keys, key_for_door(char))):
        continue
      move_keys = keys_add(current_keys, char) if is_key(char) else current_keys
      move_state = (row, col, move_keys)
      if move_state in distance:
        continue
      move_distance = current_distance + 1
      if keys_are_full(move_keys):
        return move_distance
      distance[move_state] = move_distance
      q.append(move_state)
  return None

if __name__ == '__main__':
  board = get_input()
  initial_position = find(board, '@')
  print(bfs(board, initial_position))


