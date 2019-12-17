def get_input():
  base_signal = '59793513516782374825915243993822865203688298721919339628274587775705006728427921751430533510981343323758576985437451867752936052153192753660463974146842169169504066730474876587016668826124639010922391218906707376662919204980583671961374243713362170277231101686574078221791965458164785925384486127508173239563372833776841606271237694768938831709136453354321708319835083666223956618272981294631469954624760620412170069396383335680428214399523030064601263676270903213996956414287336234682903859823675958155009987384202594409175930384736760416642456784909043049471828143167853096088824339425988907292558707480725410676823614387254696304038713756368483311'
  full_input = [int(s) for s in base_signal * 10000]
  offset = int(base_signal[:7])
  return (full_input[offset:], offset)

def iterate(input, offset, phases_count):
  current = input
  for i in range(phases_count):
    current = phase(current, offset)
  return current

class RangeSumQuery:
  def __init__(self, array):
    n = len(array)
    self.prefix = array.copy()
    for i in range(1, n):
      self.prefix[i] += self.prefix[i - 1]
    
  def sum(self, start, end):
    sum_before_start = self.prefix[start - 1] if start > 0 else 0
    return self.prefix[end] - sum_before_start

def phase(input, initial_offset):
  output = []
  n = len(input)
  rsq = RangeSumQuery(input)
  for i in range(n):
    run_length = initial_offset + i + 1
    sum_for_element = 0
    start = i
    sign = 1
    while start < n:
      end = min(start + run_length - 1, n - 1)
      sum_for_element += sign * rsq.sum(start, end)
      sign *= -1
      start += 2 * run_length
    element_value = abs(sum_for_element) % 10
    output.append(element_value)
  return output

if __name__ == '__main__':
  (input, offset) = get_input()
  result = iterate(input, offset, phases_count=100)
  first_eight_digits = result[:8]
  print(''.join([str(d) for d in first_eight_digits]))