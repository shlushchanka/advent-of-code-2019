def get_input(): 
  return (272091, 815432)

def digits(n):
  if n == 0:
    return [0]
  else:
    digits = []
    while n > 0:
      last = n % 10
      digits.append(last)
      n //= 10
    digits = list(reversed(digits))
    return digits  

def generate_valid_passwords_in_range(start, end):
  for n in range(start, end + 1):
    n_digits = digits(n)
    if is_sorted(n_digits) and has_two_equal_adjacent_digits(n_digits):
      yield n

def is_sorted(array):
  return all(array[i] <= array[i + 1] for i in range(len(array) - 1))

def has_two_equal_adjacent_digits(array):
  return any(array[i] == array[i + 1] for i in range(len(array) - 1))

if __name__ == '__main__':
  (start, end) = get_input()
  count = len(list(generate_valid_passwords_in_range(start, end)))
  print(count)