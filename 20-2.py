def get_input():
  filename = '20.txt'
  lines = []
  for line in open(filename): 
    line = line.rstrip('\n')  
    lines.append(line)
  return lines

def find_portals(board):
  from collections import defaultdict
  portals = defaultdict(list)
  (row_count, col_count) = dimensions(board)
  isValid = lambda r, c: 0 <= r < row_count and 0 <= c < col_count
  delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  for r in range(len(board)):
    for c in range(len(board[r])):
      if board[r][c] < 'A' or board[r][c] > 'Z':
        continue
      for (delta_r, delta_c) in delta:
        (free_row, free_col) = (r + delta_r, c + delta_c)
        if not isValid(free_row, free_col) or not board[free_row][free_col] == '.':
          continue
        if free_row < r or free_col < c:
          label = board[r][c] + board[r - delta_r][c - delta_c]
        else:
          label = board[r - delta_r][c - delta_c] + board[r][c]
        portals[label].append((free_row, free_col))
        break
  return portals

def split_to_outer_and_inner(board, mappings, outer_start_position):
  (r, c) = outer_start_position
  outer = set()
  outer.add(outer_start_position)
  (row_count, col_count) = dimensions(board)
  directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 1)]
  for (d_row, d_col) in directions:
    while board[r + d_row][c + d_col] == '.' or board[r + d_row][c + d_col] == '#':
      if board[r + d_row][c + d_col] == '.':
        outer.add((r + d_row, c + d_col))
      r += d_row
      c += d_col
  inner = set()
  for m in mappings:
    if m in outer:
      inner.add(mappings[m])
  return (outer, inner)

def dimensions(board):
  return (len(board), len(board[0]))

def position_mappings(portals):
  mappings = {}
  for label in portals:
    positions = portals[label]
    if len(positions) == 1:
      continue
    mappings[positions[0]] = positions[1]
    mappings[positions[1]] = positions[0]
  return mappings

def bfs(board, portals):
  from collections import deque
  initial_position = portals['AA'][0]
  initial_state = (initial_position, 0)
  mappings = position_mappings(portals)
  (outer, inner) = split_to_outer_and_inner(board, mappings, initial_position)
  steps = { initial_state: 0 }
  q = deque([initial_state])
  (row_count, col_count) = dimensions(board)
  isValid = lambda r, c: 0 <= r < row_count and 0 <= c < col_count
  directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  finish_point = portals['ZZ'][0]
  finish_state = (finish_point, 0)
  while len(q) > 0 and finish_state not in steps:
    current_state = q.popleft()
    (current_position, current_level) = current_state
    (current_row, current_col) = current_position
    next_steps = steps[current_state] + 1
    
    for (dir_row, dir_col) in directions:
      (next_row, next_col) = (current_row + dir_row, current_col + dir_col)
      next_position = (next_row, next_col)
      next_state = (next_position, current_level)
      if not isValid(next_row, next_col) or board[next_row][next_col] != '.' or next_state in steps:
        continue
      steps[next_state] = next_steps
      q.append(next_state)

    if not current_position in mappings:
      continue
    if current_position in outer:
      if current_position != initial_position and current_position != finish_point and current_level > 0:
        to_position = mappings[current_position]
        to_state = (to_position, current_level - 1)
        if to_state not in steps:
          steps[to_state] = next_steps
          q.append(to_state)
      elif current_state == finish_state:
        steps[finish_state] = next_steps
        return next_steps
    elif current_position in inner:
      to_position = mappings[current_position]
      to_state = (to_position, current_level + 1)
      if to_state not in steps:
        steps[to_state] = next_steps
        q.append(to_state)
  assert finish_state in steps
  return steps[finish_state]      


if __name__ == '__main__':
  board = get_input()
  portals = find_portals(board)
  print(bfs(board, portals))


