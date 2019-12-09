class Memory:
  def __init__(self, predefined_memory):
    from collections import defaultdict
    self.memory = defaultdict(lambda: 0)
    for i in range(len(predefined_memory)):
      self.memory[i] = predefined_memory[i]
    self.address_pointer = 0

  def read_from_address(self, address):
    return self.memory[address]

  def read_and_move_pointer(self):
    value = self.read_from_address(self.address_pointer)
    self.move_address_pointer(distance=1)
    return value
  
  def write_to_address(self, address, value):
    self.memory[address] = value

  def set_address_pointer(self, address):
    self.address_pointer = address

  def move_address_pointer(self, distance):
    self.set_address_pointer(self.address_pointer + distance)

from enum import Enum
class ReadMode(Enum):
  POSITIONAL = 0
  IMMIDIATE = 1
  RELATIVE = 2

class IntCodeComputer:

  def __init__(self, memory, std_in, std_out):
    self.memory = Memory(memory)
    self.std_in = std_in
    self.std_out = std_out
    self._is_halted = False
    self._is_waiting_for_input = False
    self.relative_base = 0
    self.operations = {
      1: self.sum,
      2: self.multiply, 
      3: self.input,
      4: self.output,
      5: self.jump_if_true,
      6: self.jump_if_false,
      7: self.less_than,
      8: self.equals,
      9: self.adjust_relative_base,
      99: self.halt
    }  
  
  @property
  def is_halted(self):
    return self._is_halted

  @property
  def has_input(self):
    return len(self.std_in) > 0

  @property
  def is_waiting_for_input(self):
    return self._is_waiting_for_input

  @is_waiting_for_input.setter
  def is_waiting_for_input(self, value):
    self._is_waiting_for_input = value

  def pop_parameter(self, read_mode):
    value_at_address = self.memory.read_and_move_pointer()
    if read_mode == ReadMode.IMMIDIATE:
      return value_at_address
    elif read_mode == ReadMode.POSITIONAL:
      return self.memory.read_from_address(value_at_address)
    elif read_mode == ReadMode.RELATIVE:
      absolute_address = self.relative_base + value_at_address
      return self.memory.read_from_address(absolute_address)

  def pop_parameters(self, parameters_modes, parameters_count, last_is_write_address=False):
    values = []
    for i in range(parameters_count):
      if i == parameters_count - 1 and last_is_write_address:
        read_mode = ReadMode.IMMIDIATE
      elif i < len(parameters_modes):
        read_mode = parameters_modes[i]
      else:
        read_mode = ReadMode.POSITIONAL
      values.append(self.pop_parameter(read_mode))
    return values

  def run(self):
    if self.is_waiting_for_input and self.has_input:
      self.is_waiting_for_input = False

    while not self.is_halted and not self.is_waiting_for_input:
      instruction = self.memory.read_and_move_pointer()
      (operation_code, parameter_modes) = self.parse_instruction(instruction)
      if operation_code not in self.operations:
        instruction_address = self.memory.address_pointer - 1
        exception_message = 'Unknown opcode %d at positon %d' % (operation_code, instruction_address)
        raise Exception(exception_message)
      else:
        operation = self.operations[operation_code]
        operation(parameter_modes)

  def write_result_of_f(self, parameter_modes, f):
    (a, b, address) = self.pop_parameters(parameter_modes, parameters_count=3, last_is_write_address=True)
    if len(parameter_modes) == 3 and parameter_modes[2] == ReadMode.RELATIVE:
      address += self.relative_base
    self.memory.write_to_address(address, value=f(a, b)) 

  def sum(self, parameter_modes):
    self.write_result_of_f(parameter_modes, f=lambda a, b: a + b)

  def multiply(self, parameter_modes):
    self.write_result_of_f(parameter_modes, f=lambda a, b: a * b)

  def input(self, parameter_modes):
    (address,) = self.pop_parameters(parameter_modes, parameters_count=1, last_is_write_address=True)
    if parameter_modes[0] == ReadMode.RELATIVE:
      address += self.relative_base
    if not self.has_input:
      self.memory.move_address_pointer(distance=-2)
      self.is_waiting_for_input = True
    else:
      in_value = self.std_in.pop(0)
      self.memory.write_to_address(address, value=in_value)

  def output(self, parameter_modes):
    (out_value,) = self.pop_parameters(parameter_modes, parameters_count=1)
    self.std_out.append(out_value)

  def jump_if_true(self, parameter_modes):
    self.jump_if_predicate(parameter_modes, predicate=bool)

  def jump_if_false(self, parameter_modes):
    self.jump_if_predicate(parameter_modes, predicate=lambda n: not bool(n))

  def jump_if_predicate(self, parameter_modes, predicate):
    (value, jump_address) = self.pop_parameters(parameter_modes, parameters_count=2)
    if predicate(value):
      self.memory.set_address_pointer(jump_address)

  def less_than(self, parameter_modes):
    self.write_result_of_f(parameter_modes, f=lambda a,b: int(a < b))

  def equals(self, parameter_modes):
    self.write_result_of_f(parameter_modes, f=lambda a,b: int(a == b))

  def adjust_relative_base(self, parameter_modes):
    (adjustment,) = self.pop_parameters(parameter_modes, parameters_count=1)
    self.relative_base += adjustment

  def halt(self, parameter_modes):
    self._is_halted = True

  def parse_instruction(self, instruction):
    operation_code = instruction % 100
    instruction //= 100
    parameter_modes = []
    while instruction > 0:
      mode_value = instruction % 10
      if mode_value == 0:
        mode = ReadMode.POSITIONAL
      elif mode_value == 1:
        mode = ReadMode.IMMIDIATE
      elif mode_value == 2:
        mode = ReadMode.RELATIVE
      parameter_modes.append(mode)
      instruction //= 10
    return (operation_code, parameter_modes)

def run_for_std_out(input):
  computer = IntCodeComputer(input, std_in=[], std_out=[])
  computer.run()
  return computer.std_out

def test_day_9():
  assert run_for_std_out([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]) == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
  assert run_for_std_out([1102,34915192,34915192,7,4,7,99,0]) == [1219070632396864]
  assert run_for_std_out([104,1125899906842624,99]) == [1125899906842624]
  print('Day 9 Works')


if __name__ == '__main__':
  test_day_9()
