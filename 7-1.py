class IntCodeComputer:
  def __init__(self, memory, std_in, std_out):
    self.memory = memory
    self.std_in = std_in
    self.std_out = std_out
    self.address_pointer = 0

  def read_from_std_in(self):
    return self.std_in.pop(0)

  def write_to_std_out(self, value):
    self.std_out.append(value)

  def read_from_address(self, address):
    return self.memory[address]

  def read_and_move_pointer(self):
    value = self.read_from_address(self.address_pointer)
    self.set_address_pointer(self.address_pointer + 1)
    return value
  
  def write_to_address(self, address, value):
    self.memory[address] = value

  def set_address_pointer(self, address):
    self.address_pointer = address

  def reached_end_of_memory(self):
    return self.address_pointer >= len(self.memory)

from enum import Enum
class ReadMode(Enum):
  POSITIONAL = 0
  IMMIDIATE = 1

def pop_parameter(vm, read_mode):
  value_at_address = vm.read_and_move_pointer()
  if read_mode == ReadMode.IMMIDIATE:
    return value_at_address
  else:
    return vm.read_from_address(value_at_address)

def pop_parameters(vm, parameters_modes, parameters_count):
  values = []
  for i in range(parameters_count):
    mode = parameters_modes[i] if i < len(parameters_modes) else ReadMode.POSITIONAL
    values.append(pop_parameter(vm, mode))
  return values

def run(memory, std_in, std_out):
  vm = IntCodeComputer(memory, std_in, std_out)
  operations = {
    1: sum,
    2: multiply, 
    3: input,
    4: output,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    99: halt
  }
  while not vm.reached_end_of_memory():
    (operation_code, parameter_modes) = parse_instruction(vm.read_and_move_pointer())
    if operation_code not in operations:
      exception_message = 'Unknown opcode %d at positon %d' % (operation_code, vm.address_pointer - 1)
      raise Exception(exception_message)
    else:
      operation = operations[operation_code]
      operation(vm, parameter_modes)

def write_result_of_f(vm, parameter_modes, f):
  (a, b) = pop_parameters(vm, parameter_modes, parameters_count=2)
  address = vm.read_and_move_pointer()
  vm.write_to_address(address, value=f(a, b)) 

def sum(vm, parameter_modes):
  write_result_of_f(vm, parameter_modes, f=lambda a, b: a + b)

def multiply(vm, parameter_modes):
  write_result_of_f(vm, parameter_modes, f=lambda a, b: a * b)

def input(vm, parameter_modes):
  address = vm.read_and_move_pointer()
  in_value = vm.read_from_std_in()
  vm.write_to_address(address, value=in_value)

def output(vm, parameter_modes):
  (out_value,) = pop_parameters(vm, parameter_modes, parameters_count=1)
  vm.write_to_std_out(out_value)

def jump_if_true(vm, parameter_modes):
  jump_if_predicate(vm, parameter_modes, predicate=bool)

def jump_if_false(vm, parameter_modes):
  jump_if_predicate(vm, parameter_modes, predicate=lambda n: not bool(n))

def jump_if_predicate(vm, parameter_modes, predicate):
  (value, jump_address) = pop_parameters(vm, parameter_modes, parameters_count=2)
  if predicate(value):
    vm.set_address_pointer(jump_address)

def less_than(vm, parameter_modes):
  write_result_of_f(vm, parameter_modes, f=lambda a,b: int(a < b))

def equals(vm, parameter_modes):
  write_result_of_f(vm, parameter_modes, f=lambda a,b: int(a == b))

def halt(vm, parameter_modes):
  vm.set_address_pointer(len(vm.memory))

def parse_instruction(instruction):
  operation_code = instruction % 100
  instruction //= 100
  parameter_modes = []
  while instruction > 0:
    mode_value = instruction % 10
    mode = ReadMode.POSITIONAL if mode_value == 0 else ReadMode.IMMIDIATE
    parameter_modes.append(mode)
    instruction //= 10
  return (operation_code, parameter_modes)

def get_input():
  return [3,8,1001,8,10,8,105,1,0,0,21,30,39,64,81,102,183,264,345,426,99999,3,9,1001,9,2,9,4,9,99,3,9,1002,9,4,9,4,9,99,3,9,1002,9,5,9,101,2,9,9,102,3,9,9,1001,9,2,9,1002,9,2,9,4,9,99,3,9,1002,9,3,9,1001,9,5,9,1002,9,3,9,4,9,99,3,9,102,4,9,9,1001,9,3,9,102,4,9,9,1001,9,5,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,99]

def run_circuit(program, phases):
  previous_output = 0
  for i in range(len(phases)):
    phase_setting = phases[i]
    std_in = [phase_setting, previous_output]
    std_out = []
    run(program.copy(), std_in, std_out)
    previous_output = std_out[0]
  return previous_output

def find_max(program, phases_count):
  max_signal = 0
  phases = list(range(phases_count))
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
  print(find_max(program, 5))