from IntCodeComputer import IntCodeComputer

def get_input():
  return [3,8,1001,8,10,8,105,1,0,0,21,30,39,64,81,102,183,264,345,426,99999,3,9,1001,9,2,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,1002,9,5,9,101,2,9,9,102,3,9,9,1001,9,2,9,1002,9,2,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,1002,9,3,9,4,9,99,3,9,102,4,9,9,1001,9,3,9,102,4,9,9,1001,9,5,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,99]

def run_circuit(program, phases):
  std_outs = [ [] for i in range(len(phases)) ]
  computers = []
  for i in range(len(phases)):
    phases_count = len(phases)
    previous_index = (phases_count + i - 1) % phases_count
    std_in = std_outs[previous_index]
    std_in.append(phases[i])
    std_out = std_outs[i]
    memory = program.copy()
    computers.append(IntCodeComputer(memory, std_in, std_out))
  computers[0].std_in.append(0)

  any_waiting_for_input = True
  while any_waiting_for_input:
    any_waiting_for_input = False
    for c in computers:
      if c.is_halted:
        continue
      c.run()
      any_waiting_for_input = any_waiting_for_input or c.is_waiting_for_input
      
  return std_outs[-1][0]

def find_max(program, phases):
  max_signal = 0
  has_next = True
  while has_next:
    max_signal = max(max_signal, run_circuit(program, phases))
    has_next = next_permutation(phases)
  return max_signal

def next_permutation(values):
  i = len(values) - 2
  while i >= 0 and values[i] >= values[i + 1]:
    i -= 1
  if i == -1:
    reverse(values, 0, len(values) - 1)
    return False
  else:
    first_greater_index = len(values) - 1
    while values[i] >= values[first_greater_index]:
      first_greater_index -= 1
    swap(values, i, first_greater_index)
    reverse(values, i + 1, len(values) - 1)
    return True

def reverse(values, start, end):
  while start < end:
    swap(values, start, end)
    start += 1
    end -= 1
  
def swap(values, i, j):
  values[i], values[j] = values[j], values[i]

if __name__ == '__main__':
  program = get_input()
  print(find_max(program, phases=list(range(5, 10))))