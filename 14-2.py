def get_input():
  filename = '14.txt'
  recipes = {}
  for line in open(filename):
    line = line.rstrip('\n')  
    import re
    all_ingridients = [parse_to_ingridient(s) for s in re.findall(r'(\d+ \w+)', line)]
    input_ingridients = all_ingridients[:-1]
    (quantity, chemical) = all_ingridients[-1]
    recipes[chemical] = (quantity, input_ingridients)
  return recipes

def ingridient(quantity, chemical):
  return (quantity, chemical)

def quantity(ingridient):
  return ingridient[0]

def chemical(ingridient):
  return ingridient[1]

def parse_to_ingridient(string):
  parts = [s.strip() for s in string.strip().split(' ')]
  return ingridient(quantity=int(parts[0]), chemical=parts[1])

def expand(recipe, fuel_quantity):
  got = {chemical: 0 for chemical in recipe}
  need = {chemical: 0 for chemical in recipe}
  got['ORE'] = need['ORE'] = 0
  need['FUEL'] = fuel_quantity
  while any([c != 'ORE' and need[c] > 0 for c in need]):
    for chemical in need:
      if chemical == 'ORE' or need[chemical] == 0: 
        continue
      if got[chemical] < need[chemical]:
        need[chemical] -= got[chemical]
        got[chemical] = 0
        (reaction_quantity, reaction_ingridients) = recipe[chemical]
        from math import ceil
        repeat = ceil(need[chemical] / reaction_quantity)
        for (reaction_chemical_quantity, reaction_chemical) in reaction_ingridients:
          need[reaction_chemical] += repeat * reaction_chemical_quantity
        got[chemical] = reaction_quantity * repeat
      got[chemical] -= need[chemical]
      need[chemical] = 0
  return need['ORE']  

if __name__ == '__main__':
  recipe = get_input()
  ore_for_one_fuel = expand(recipe, 1)
  ore_available = 10 ** 12
  lo = ore_available // ore_for_one_fuel
  hi = lo * 4
  while lo <= hi:
    mid = lo + (hi - lo) // 2
    if expand(recipe, fuel_quantity=mid) <= ore_available:
      lo = mid + 1
    else:
      hi = mid - 1
  print(hi)