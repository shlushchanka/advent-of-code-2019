def count_orbits(graph):
  vertex_to_subtree_size = {}
  sum = 0
  for v in graph.keys():
    sum += dfs(graph, vertex_to_subtree_size, v)
  return sum

def dfs(graph, vertex_to_subtree_size, v):
  if v not in vertex_to_subtree_size:
    size = len(graph[v])
    for child in graph[v]:
      size += dfs(graph, vertex_to_subtree_size, child)
    vertex_to_subtree_size[v] = size
  return vertex_to_subtree_size[v]

def get_input(): 
  from collections import defaultdict
  graph = defaultdict(list)
  filename = '6.txt'
  lines = [line.rstrip('\n') for line in open(filename)]
  for line in lines:
    (parent, child) = line.split(')')
    graph[parent].append(child)
  return graph

if __name__ == '__main__':
  graph = get_input()
  print(count_orbits(graph))