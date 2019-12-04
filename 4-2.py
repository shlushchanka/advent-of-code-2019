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
      n /= 10
    digits = list(reversed(digits))
    return digits  

def generate_valid_passwords_in_range(start, end):
  for n in range(start, end + 1):
    n_digits = digits(n)
    if is_sorted(n_digits) and has_group_of_exactly_two_matching_digits(n_digits):
      yield n

def is_sorted(array):
  return all(array[i] <= array[i + 1] for i in xrange(len(array) - 1))

def has_group_of_exactly_two_matching_digits(array):
  count = 1
  for i in xrange(1, len(array)):
    if array[i - 1] == array[i]:
      count += 1
    elif count == 2:
      return True
    else:
      count = 1
  return count == 2

if __name__ == '__main__':
  (start, end) = get_input()
  count = len(list(generate_valid_passwords_in_range(start, end)))
  print(count)