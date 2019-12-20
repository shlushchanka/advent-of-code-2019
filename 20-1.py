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
  mappings = position_mappings(portals)
  initial_position = portals['AA'][0]
  steps = { initial_position: 0 }
  q = deque([initial_position])
  (row_count, col_count) = dimensions(board)
  isValid = lambda r, c: 0 <= r < row_count and 0 <= c < col_count
  directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  finish_point = portals['ZZ'][0]
  while len(q) > 0 and finish_point not in steps:
    (current_row, current_col) = q.popleft()
    current_steps = steps[(current_row, current_col)]
    for (dir_row, dir_col) in directions:
      (next_row, next_col) = (current_row + dir_row, current_col + dir_col)
      if not isValid(next_row, next_col) or board[next_row][next_col] != '.' or (next_row, next_col) in steps:
        continue
      steps[(next_row, next_col)] = current_steps + 1
      q.append((next_row, next_col))
    if (current_row, current_col) in mappings:
      to_position = mappings[(current_row, current_col)]
      if to_position not in steps:
        steps[to_position] = current_steps + 1
        q.append(to_position)
  assert finish_point in steps
  return steps[finish_point]      


if __name__ == '__main__':
  board = get_input()
  portals = find_portals(board)
  print(bfs(board, portals))


