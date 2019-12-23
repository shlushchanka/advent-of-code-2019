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

  def __init__(self, memory, std_in=[], std_out=[]):
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

  def pop_parameters(self, parameters_modes, parameters_count, last_is_write_address=False):
    values = []
    for i in range(parameters_count):
      if i == parameters_count - 1 and last_is_write_address:
        read_mode = parameters_modes[i] if i < len(parameters_modes) else ReadMode.IMMIDIATE
        values.append(self.pop_write_address(read_mode))
      else:
        read_mode = parameters_modes[i] if i < len(parameters_modes) else ReadMode.POSITIONAL
        values.append(self.pop_operand(read_mode))
    return values

  def pop_operand(self, read_mode):
    value_at_address = self.memory.read_and_move_pointer()
    if read_mode == ReadMode.IMMIDIATE:
      return value_at_address
    elif read_mode == ReadMode.POSITIONAL:
      return self.memory.read_from_address(value_at_address)
    elif read_mode == ReadMode.RELATIVE:
      absolute_address = self.relative_base + value_at_address
      return self.memory.read_from_address(absolute_address)

  def pop_write_address(self, read_mode):
    if read_mode == ReadMode.IMMIDIATE:
      return self.memory.read_and_move_pointer()
    elif read_mode == ReadMode.RELATIVE:
      relative_address = self.memory.read_and_move_pointer()
      return self.relative_base + relative_address

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
    (a, b, write_address) = self.pop_parameters(parameter_modes, parameters_count=3, last_is_write_address=True)
    self.memory.write_to_address(write_address, value=f(a, b)) 

  def sum(self, parameter_modes):
    self.write_result_of_f(parameter_modes, f=lambda a, b: a + b)

  def multiply(self, parameter_modes):
    self.write_result_of_f(parameter_modes, f=lambda a, b: a * b)

  def input(self, parameter_modes):
    (write_address,) = self.pop_parameters(parameter_modes, parameters_count=1, last_is_write_address=True)
    if not self.has_input:
      self.memory.move_address_pointer(distance=-2)
      self.is_waiting_for_input = True
    else:
      in_value = self.std_in.pop(0)
      self.memory.write_to_address(write_address, value=in_value)

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
    
  def read_int(self):
    return self.std_out.pop(0)

  def read_ints(self, at_most):
    read = []
    length = min(len(self.std_out), at_most)
    for i in range(length):
      read.append(self.read_int())
    return read
  
  def read_char(self):
    return ord(self.read_int())

  def write_int(self, value):
    self.std_in.append(value)

  def write_ints(self, values):
    self.std_in.extend(values)

  def read_line(self):
    c = self.read_char()
    read = []
    while c != '\n':
      read.append(c)
    return ''.join(read)

  def write_char(self, value):
    self.write_int(ord(value))

  def write_line(self, line):
    for c in line:
      self.write_char(c)
    self.write_char('\n')

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
  # test_day_9()
  input = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,3,0,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,1,344,1023,1101,0,0,1020,1101,0,481,1024,1102,1,1,1021,1101,0,24,1005,1101,0,29,1018,1102,39,1,1019,1102,313,1,1028,1102,1,35,1009,1101,28,0,1001,1101,26,0,1013,1101,0,351,1022,1101,564,0,1027,1102,1,32,1011,1101,23,0,1006,1102,1,25,1015,1101,21,0,1003,1101,0,31,1014,1101,33,0,1004,1102,37,1,1000,1102,476,1,1025,1101,22,0,1007,1102,30,1,1012,1102,1,27,1017,1102,1,34,1002,1101,38,0,1008,1102,1,36,1010,1102,1,20,1016,1102,567,1,1026,1102,1,304,1029,109,-6,2108,35,8,63,1005,63,201,1001,64,1,64,1106,0,203,4,187,1002,64,2,64,109,28,21101,40,0,-9,1008,1013,38,63,1005,63,227,1001,64,1,64,1105,1,229,4,209,1002,64,2,64,109,-2,1205,1,243,4,235,1105,1,247,1001,64,1,64,1002,64,2,64,109,-12,2102,1,-5,63,1008,63,24,63,1005,63,271,1001,64,1,64,1105,1,273,4,253,1002,64,2,64,109,8,2108,22,-9,63,1005,63,295,4,279,1001,64,1,64,1106,0,295,1002,64,2,64,109,17,2106,0,-5,4,301,1001,64,1,64,1106,0,313,1002,64,2,64,109,-21,21107,41,40,7,1005,1019,333,1001,64,1,64,1105,1,335,4,319,1002,64,2,64,109,1,2105,1,10,1001,64,1,64,1105,1,353,4,341,1002,64,2,64,109,10,1206,-3,371,4,359,1001,64,1,64,1105,1,371,1002,64,2,64,109,-5,21108,42,42,-7,1005,1011,393,4,377,1001,64,1,64,1105,1,393,1002,64,2,64,109,-8,2101,0,-4,63,1008,63,23,63,1005,63,415,4,399,1105,1,419,1001,64,1,64,1002,64,2,64,109,13,21102,43,1,-6,1008,1017,43,63,1005,63,441,4,425,1106,0,445,1001,64,1,64,1002,64,2,64,109,-21,1207,0,33,63,1005,63,465,1001,64,1,64,1106,0,467,4,451,1002,64,2,64,109,19,2105,1,3,4,473,1106,0,485,1001,64,1,64,1002,64,2,64,109,1,21101,44,0,-7,1008,1015,44,63,1005,63,511,4,491,1001,64,1,64,1106,0,511,1002,64,2,64,109,2,1206,-3,527,1001,64,1,64,1105,1,529,4,517,1002,64,2,64,109,-8,1201,-7,0,63,1008,63,35,63,1005,63,555,4,535,1001,64,1,64,1105,1,555,1002,64,2,64,109,1,2106,0,10,1105,1,573,4,561,1001,64,1,64,1002,64,2,64,109,4,21107,45,46,-7,1005,1014,591,4,579,1106,0,595,1001,64,1,64,1002,64,2,64,109,-12,1208,-6,21,63,1005,63,617,4,601,1001,64,1,64,1105,1,617,1002,64,2,64,109,-11,1208,6,31,63,1005,63,637,1001,64,1,64,1106,0,639,4,623,1002,64,2,64,109,16,2101,0,-7,63,1008,63,20,63,1005,63,659,1105,1,665,4,645,1001,64,1,64,1002,64,2,64,109,3,2102,1,-9,63,1008,63,38,63,1005,63,691,4,671,1001,64,1,64,1106,0,691,1002,64,2,64,109,4,1205,-1,703,1105,1,709,4,697,1001,64,1,64,1002,64,2,64,109,-14,21108,46,45,7,1005,1014,729,1001,64,1,64,1105,1,731,4,715,1002,64,2,64,109,7,21102,47,1,0,1008,1014,45,63,1005,63,755,1001,64,1,64,1106,0,757,4,737,1002,64,2,64,109,-12,2107,34,7,63,1005,63,775,4,763,1105,1,779,1001,64,1,64,1002,64,2,64,109,-5,1207,6,22,63,1005,63,797,4,785,1106,0,801,1001,64,1,64,1002,64,2,64,109,12,1202,0,1,63,1008,63,35,63,1005,63,827,4,807,1001,64,1,64,1105,1,827,1002,64,2,64,109,-5,1202,0,1,63,1008,63,36,63,1005,63,851,1001,64,1,64,1105,1,853,4,833,1002,64,2,64,109,-2,1201,4,0,63,1008,63,20,63,1005,63,873,1105,1,879,4,859,1001,64,1,64,1002,64,2,64,109,2,2107,22,-1,63,1005,63,899,1001,64,1,64,1106,0,901,4,885,4,64,99,21102,1,27,1,21101,0,915,0,1105,1,922,21201,1,53897,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21101,0,942,0,1106,0,922,21202,1,1,-1,21201,-2,-3,1,21101,0,957,0,1105,1,922,22201,1,-1,-2,1105,1,968,22102,1,-2,-2,109,-3,2105,1,0]
  std_in = [1]
  std_out = []
  computer = IntCodeComputer(input, std_in, std_out)
  computer.run()
  print(std_out[0])
