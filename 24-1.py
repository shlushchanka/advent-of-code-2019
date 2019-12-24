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

def count_adjacent_cells(board, r, c, symbol):
  delta = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  count = 0
  for (d_row, d_col) in delta:
    (adj_row, adj_col) = (r + d_row, c + d_col)
    if 0 <= adj_row < row_count and 0 <= adj_col < col_count and board[adj_row][adj_col] == symbol:
      count += 1
  return count

def iterate_game_of_life(board):
  next = []
  for r in range(row_count):
    row = board[r].copy()
    next.append(row)
  for r in range(row_count):
    for c in range(col_count):
      bugs = count_adjacent_cells(board, r, c, BUG)
      if board[r][c] == BUG and bugs != 1:
        next[r][c] = FREE
      elif board[r][c] == FREE and 1 <= bugs <= 2:
        next[r][c] = BUG
      else: 
        next[r][c] = board[r][c]
  return next

def find_biodiversity_rating(board):
  seen = set()
  current = board
  current_mask = mask(current)
  while current_mask not in seen:
    seen.add(current_mask)
    current = iterate_game_of_life(current)
    current_mask = mask(current)
  return current_mask

if __name__ == '__main__':
  board = get_input()
  print(find_biodiversity_rating(board))