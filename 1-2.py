def fuel_for_mass(module_mass):
  return sum(fixed_point_generator(raw_fuel_for_mass, module_mass)) - module_mass

def fixed_point_generator(f, x): 
  yield x
  next_x = f(x)
  while next_x != x:
    yield next_x
    x = next_x
    next_x = f(x)

def raw_fuel_for_mass(module_mass):
  return max(module_mass / 3 - 2, 0)

# def get_input():
#   import requests as r
#   input_url = 'https://adventofcode.com/2019/day/1/input'
#   r.get('https://adventofcode.com/2019/day/1/input')

def get_input():
  return [
    119606,
    94066,
    80497,
    136413,
    83710,
    136098,
    113785,
    100655,
    148973,
    78186,
    75572,
    68954,
    140581,
    76963,
    123969,
    111620,
    106957,
    80469,
    140605,
    119650,
    112495,
    124851,
    119725,
    93118,
    123105,
    92952,
    131053,
    74500,
    135647,
    107536,
    56501,
    64458,
    115542,
    111894,
    51608,
    85570,
    133474,
    118513,
    109296,
    128000,
    87127,
    146391,
    149508,
    107219,
    70461,
    85261,
    137378,
    138297,
    106834,
    112664,
    53841,
    124055,
    96992,
    91394,
    135390,
    119457,
    84966,
    110652,
    138798,
    65060,
    108499,
    126384,
    116976,
    135353,
    52801,
    53139,
    54144,
    69494,
    52068,
    61600,
    62762,
    102578,
    100023,
    119232,
    97153,
    94554,
    114131,
    54643,
    65729,
    124430,
    106513,
    133856,
    96803,
    132140,
    113994,
    65320,
    123970,
    115693,
    129066,
    132805,
    143283,
    132702,
    109683,
    126041,
    63310,
    82628,
    68097,
    58927,
    123635,
    117809,
  ]

if __name__ == "__main__":
    input = get_input()
    fuel_list = [fuel_for_mass(mass) for mass in input] 
    fuel_sum = sum(fuel_list)
    print(fuel_sum)