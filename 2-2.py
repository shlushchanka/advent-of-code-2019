from IntCodeComputer import IntCodeComputer

def get_input():
  return [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,6,19,23,1,10,23,27,2,27,13,31,1,31,6,35,2,6,35,39,1,39,5,43,1,6,43,47,2,6,47,51,1,51,5,55,2,55,9,59,1,6,59,63,1,9,63,67,1,67,10,71,2,9,71,75,1,6,75,79,1,5,79,83,2,83,10,87,1,87,5,91,1,91,9,95,1,6,95,99,2,99,10,103,1,103,5,107,2,107,6,111,1,111,5,115,1,9,115,119,2,119,10,123,1,6,123,127,2,13,127,131,1,131,6,135,1,135,10,139,1,13,139,143,1,143,13,147,1,5,147,151,1,151,2,155,1,155,5,0,99,2,0,14,0]

def find_verb_and_noun(input, target): 
  for noun in range(0, 100):
    for verb in range(0, 100):
      opcodes = list(input)
      opcodes[1] = noun
      opcodes[2] = verb
      if evaluates_to_target(opcodes, target):
        return build_answer(noun, verb)
  else:
    raise Exception('did not found answer')

def evaluates_to_target(program, target):
  try:
    computer = IntCodeComputer(program, std_in=[], std_out=[])
    computer.run()
    return program[0] == target
  except Exception:
    return False

def build_answer(noun, verb):
  return noun * 100 + verb

if __name__ == '__main__':
  input = get_input()
  target = 19690720
  print(find_verb_and_noun(input, target))