from collections import defaultdict


def get_input():
  filename = '24.txt'
  board = []
  for line in open(filename): 
    line = line.rstrip('\n')  
    row = [c for c in line]
    board.append(row)
  return board

BUG = '#'
FREE = '.'

row_count = 5
col_count = 5

def mask(board):
  int_mask = 0
  i = 0
  for r in range(row_count):
    for c in range(col_count):
      if board[r][c] == BUG:
        int_mask |= 1 << i
      i += 1
  return int_mask

def bug_increment(symbol):
  return 1 if symbol == BUG else 0

def count_adjacent_cells(levels, current_level, r, c, symbol):
  board = levels[current_level]
  delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  count = 0
  for (d_row, d_col) in delta:
    (adj_row, adj_col) = (r + d_row, c + d_col)
    if adj_row < 0 or adj_row == row_count or adj_col < 0 or adj_col == col_count:
      count += count_rec_outer(levels[current_level - 1], d_row, d_col)
    elif board[adj_row][adj_col] == '?':
      count += count_rec_inner(levels[current_level + 1], d_row, d_col)
    else: 
      count += bug_increment(board[adj_row][adj_col])
  return count

def count_rec_outer(board, d_row, d_col):
  middle = 2
  (r, c) = (middle + d_row, middle + d_col)
  return bug_increment(board[r][c])

def count_rec_inner(board, d_row, d_col):
  count = 0
  if d_row == -1: #last row
    r = -1
    for c in range(col_count):
      count += bug_increment(board[r][c])
  elif d_row == 1: #first row
    r = 0
    for c in range(col_count):
      count += bug_increment(board[r][c])
  elif d_col == -1: #last col
    c = -1
    for r in range(row_count):
      count += bug_increment(board[r][c])
  elif d_col == 1: #first col
    c = 0
    for r in range(row_count):
      count += bug_increment(board[r][c])
  return count

def iterate_game_of_life(levels, current_level):
  board = levels[current_level]
  next = []
  for r in range(row_count):
    row = board[r].copy()
    next.append(row)
  for r in range(row_count):
    for c in range(col_count):
      bugs = count_adjacent_cells(levels, current_level, r, c, BUG)
      if board[r][c] == BUG and bugs != 1:
        next[r][c] = FREE
      elif board[r][c] == FREE and 1 <= bugs <= 2:
        next[r][c] = BUG
      else: 
        next[r][c] = board[r][c]
  return next

def count_bugs_in_recursive_board(levels, minutes):
  for minute in range(1, minutes + 1):
    next_levels = defaultdict(empty_board)
    for current_level in range (-minute, minute + 1):
      next_levels[current_level] = iterate_game_of_life(levels, current_level)
    levels = next_levels

  for current_level in levels:
    print("Depth " + str(current_level) + ":")
    print_board(levels[current_level])
  return sum([count_bugs(levels[b]) for b in levels])
  
def count_bugs(board):
  count = 0
  for r in range(row_count):
    for c in range(col_count):
      count += bug_increment(board[r][c])
  return count

def print_board(board):
  for r in board:
    print(''.join(r))

def empty_board():
  return [
    ['.', '.', '.', '.', '.'], 
    ['.', '.', '.', '.', '.'], 
    ['.', '.', '?', '.', '.'], 
    ['.', '.', '.', '.', '.'], 
    ['.', '.', '.', '.', '.']
  ]

if __name__ == '__main__':
  levels = defaultdict(empty_board)
  zero_board = get_input()
  zero_board[2][2] = '?'
  levels[0] = zero_board
  print(count_bugs_in_recursive_board(levels, minutes=200))
  