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
  return [3,225,1,225,6,6,1100,1,238,225,104,0,1001,92,74,224,1001,224,-85,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1101,14,63,225,102,19,83,224,101,-760,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1101,21,23,224,1001,224,-44,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1102,40,16,225,1102,6,15,225,1101,84,11,225,1102,22,25,225,2,35,96,224,1001,224,-350,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,56,43,225,101,11,192,224,1001,224,-37,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1002,122,61,224,1001,224,-2623,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1,195,87,224,1001,224,-12,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1101,75,26,225,1101,6,20,225,1102,26,60,224,101,-1560,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,677,226,224,102,2,223,223,1006,224,329,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,344,101,1,223,223,7,226,677,224,102,2,223,223,1006,224,359,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,374,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,389,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,404,101,1,223,223,1107,226,226,224,1002,223,2,223,1005,224,419,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,434,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,449,101,1,223,223,107,677,677,224,102,2,223,223,1005,224,464,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,479,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,524,1001,223,1,223,1008,677,677,224,102,2,223,223,1006,224,539,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,554,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,569,101,1,223,223,107,677,226,224,102,2,223,223,1005,224,584,101,1,223,223,8,226,226,224,1002,223,2,223,1005,224,599,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,614,1001,223,1,223,7,226,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1008,226,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

if __name__ == '__main__':
  opcodes = get_input()
  std_in = [5]
  std_out = []
  run(opcodes, std_in, std_out)
  print(std_out)