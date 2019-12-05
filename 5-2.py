def run(opcodes, std_in, std_out):
  ADD_OPCODE = 1
  MULTIPLY_OPCODE = 2
  INPUT_OPCODE = 3
  OUTPUT_OPCODE = 4
  JUMP_IF_TRUE = 5
  JUMP_IF_FALSE = 6
  LESS_THAN = 7
  EQUALS = 8
  HALT_OPCODE = 99
  position = 0
  while opcodes[position] != HALT_OPCODE:
    (opcode, modes) = parse(opcodes[position])
    arguments_start_address = position + 1
    if opcode == ADD_OPCODE:
      process_opcode(lambda a, b: a + b, opcodes, arguments_start_address, modes)
      position += 4
    elif opcode == MULTIPLY_OPCODE:
      process_opcode(lambda a, b: a * b, opcodes, arguments_start_address, modes)
      position += 4
    elif opcode == INPUT_OPCODE:
      in_value = std_in.pop(0)
      in_address = opcodes[position + 1]
      opcodes[in_address] = in_value
      position += 2
    elif opcode == OUTPUT_OPCODE:
      out_value = read_argument(opcodes, modes, arguments_start_address, 0)
      std_out.append(out_value)
      position += 2
    elif opcode == JUMP_IF_TRUE:
      condition = read_argument(opcodes, modes, arguments_start_address, 0)
      if condition != 0:
        position = read_argument(opcodes, modes, arguments_start_address, 1)
      else:
        position += 3
    elif opcode == JUMP_IF_FALSE:
      condition = read_argument(opcodes, modes, arguments_start_address, 0)
      if condition == 0:
        position = read_argument(opcodes, modes, arguments_start_address, 1)
      else:
         position += 3
    elif opcode == LESS_THAN:
      first_argument = read_argument(opcodes, modes, arguments_start_address, 0)
      second_argument = read_argument(opcodes, modes, arguments_start_address, 1)
      third_argument = opcodes[arguments_start_address + 2]
      if first_argument < second_argument:
        opcodes[third_argument] = 1
      else:
        opcodes[third_argument] = 0
      position += 4
    elif opcode == EQUALS:
      first_argument = read_argument(opcodes, modes, arguments_start_address, 0)
      second_argument = read_argument(opcodes, modes, arguments_start_address, 1)
      third_argument = opcodes[arguments_start_address + 2]
      if first_argument == second_argument:
        opcodes[third_argument] = 1
      else:
        opcodes[third_argument] = 0
      position += 4
    elif opcode == HALT_OPCODE:
      return
    else:
      exception_message = 'Unknown opcode %d at positon %d' % (opcode, position)
      raise Exception(exception_message)
  return opcodes[0]

def read_argument(opcodes, modes, arguments_start_address, index):
  mode = read_mode(modes, index)
  address = arguments_start_address + index
  address_value = opcodes[address]
  if mode == 0:
    return opcodes[address_value]
  else:
    return address_value

def parse(instruction):
  opcode = instruction % 100
  instruction //= 100
  modes = []
  while instruction > 0:
    mode = instruction % 10
    modes.append(mode)
    instruction //= 10
  return (opcode, modes)

def process_opcode(operation, opcodes, arguments_position, modes):
  first_arg = read_argument(opcodes, modes, arguments_position, 0)
  second_arg = read_argument(opcodes, modes, arguments_position, 1)
  result = operation(first_arg, second_arg)
  result_address = opcodes[arguments_position + 2]
  opcodes[result_address] = result

def read_mode(modes, index):
  return modes[index] if len(modes) > 0 and index < len(modes) else 0

def get_input():
  return [3,225,1,225,6,6,1100,1,238,225,104,0,1001,92,74,224,1001,224,-85,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1101,14,63,225,102,19,83,224,101,-760,224,224,4,224,102,8,223,223,101,2,224,224,1,224,223,223,1101,21,23,224,1001,224,-44,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1102,40,16,225,1102,6,15,225,1101,84,11,225,1102,22,25,225,2,35,96,224,1001,224,-350,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,1101,56,43,225,101,11,192,224,1001,224,-37,224,4,224,102,8,223,223,1001,224,4,224,1,223,224,223,1002,122,61,224,1001,224,-2623,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1,195,87,224,1001,224,-12,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,1101,75,26,225,1101,6,20,225,1102,26,60,224,101,-1560,224,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,108,677,226,224,102,2,223,223,1006,224,329,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,344,101,1,223,223,7,226,677,224,102,2,223,223,1006,224,359,1001,223,1,223,1007,226,677,224,1002,223,2,223,1006,224,374,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,389,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,404,101,1,223,223,1107,226,226,224,1002,223,2,223,1005,224,419,1001,223,1,223,1007,677,677,224,102,2,223,223,1006,224,434,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,449,101,1,223,223,107,677,677,224,102,2,223,223,1005,224,464,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,479,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,524,1001,223,1,223,1008,677,677,224,102,2,223,223,1006,224,539,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,554,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,569,101,1,223,223,107,677,226,224,102,2,223,223,1005,224,584,101,1,223,223,8,226,226,224,1002,223,2,223,1005,224,599,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,614,1001,223,1,223,7,226,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1107,677,226,224,102,2,223,223,1005,224,644,101,1,223,223,8,226,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1008,226,677,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

if __name__ == '__main__':
  opcodes = get_input()
  std_in = [5]
  std_out = []
  run(opcodes, std_in, std_out)
  print(std_out)