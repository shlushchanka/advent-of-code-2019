def get_input():
  filename = '22.txt'
  lines = []
  for line in open(filename): 
    line = line.rstrip('\n')  
    lines.append(line)
  return lines

def deal_into_new_stack(cards):
  cards.reverse()
  return cards

def cut(cards, n):
  if n >= 0:
    top = cards[:n]
    rest = cards[n:]
    rest.extend(top)
    return rest
  else:
    head = cards[:n]
    tail = cards[n:]
    tail.extend(head)
    return tail

def deal_with_increment(cards, n):
  length = len(cards)
  out = list(range(length))
  out_index = 0
  cards_index = 0
  while cards_index < length:
    out[out_index] = cards[cards_index]
    out_index = (out_index + n) % length
    cards_index += 1
  return out

def split_to_command_and_integer(s):
  split_index = len(s) - 1
  while s[split_index] != ' ':
    split_index -= 1
  return (s[0:split_index], int(s[split_index + 1:]))

def process_instructions(cards, instructions):
  for instruction in instructions:
    if instruction == 'deal into new stack':
      cards = deal_into_new_stack(cards)
    else: 
      (command, n) = split_to_command_and_integer(instruction)
      if command == 'cut':
        cards = cut(cards, n)
      elif command == 'deal with increment':
        cards = deal_with_increment(cards, n)
  return cards

def find_index(cards, card_value):
  i = 0
  while i < len(cards):
    if cards[i] == card_value:
      return i
    else:
      i += 1
  return -1

if __name__ == '__main__':
  input = get_input()
  deck_size = 10007
  cards = list(range(deck_size))
  cards = process_instructions(cards, input)
  print(find_index(cards, 2019))
