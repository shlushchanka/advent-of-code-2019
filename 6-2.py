def distance(graph, source, dest):
  from collections import deque
  q = deque(['YOU'])
  distance = { source: 0 }  
  while len(q) > 0 and dest not in q:
    current = q.pop()
    for to in graph[current]:
      if to not in distance:
        distance[to] = distance[current] + 1
        q.append(to)
  return distance[dest]

def get_input(): 
  from collections import defaultdict
  graph = defaultdict(list)
  filename = '6.txt'
  lines = [line.rstrip('\n') for line in open(filename)]
  for line in lines:
    (parent, child) = line.split(')')
    graph[parent].append(child)
    graph[child].append(parent)
  return graph

if __name__ == '__main__':
  graph = get_input()
  print(distance(graph, 'YOU', 'SAN') - 2)