def full_pattern(length, repeat):
  pattern = [0, 1, 0, -1]
  pattern_index = 0
  full = []
  end_length = length + 1
  while len(full) < end_length:
    for i in range(min(repeat, end_length - len(full))):
      full.append(pattern[pattern_index])
    pattern_index = (pattern_index + 1) % len(pattern)
  full.pop(0)
  return full

def dot_product(xs, ys):
  return [x * y for (x, y) in zip(xs, ys)]

def phase(input_list, patterns):
  output = []
  for i in range(len(input_list)):
    full_pattern = patterns[i]
    product = dot_product(input_list, full_pattern)
    result = sum(product)
    output.append(abs(result) % 10)
  return output

def get_input():
  return [int(s) for s in '59793513516782374825915243993822865203688298721919339628274587775705006728427921751430533510981343323758576985437451867752936052153192753660463974146842169169504066730474876587016668826124639010922391218906707376662919204980583671961374243713362170277231101686574078221791965458164785925384486127508173239563372833776841606271237694768938831709136453354321708319835083666223956618272981294631469954624760620412170069396383335680428214399523030064601263676270903213996956414287336234682903859823675958155009987384202594409175930384736760416642456784909043049471828143167853096088824339425988907292558707480725410676823614387254696304038713756368483311']

def iterate(input, source_pattern, phases_count):
  full_patterns = []
  for i in range(len(input)):
    full_patterns.append(full_pattern(len(input), repeat=i + 1))
  current = input
  for i in range(phases_count):
    current = phase(current, full_patterns)
  return current

if __name__ == '__main__':
  input = get_input()
  result = iterate(input, source_pattern=[1, 0, -1, 0], phases_count=100)
  first_eight_digits = result[:8]
  print(''.join([str(d) for d in first_eight_digits]))