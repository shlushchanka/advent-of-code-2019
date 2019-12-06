def count_orbits(graph):
  vertex_to_subtree_size = {}
  for v in graph.keys():
    if v not in vertex_to_subtree_size:
      dfs(graph, vertex_to_subtree_size, v)
  counts = vertex_to_subtree_size.values()
  return sum(counts)

def dfs(graph, vertex_to_subtree_size, v):
  if v not in graph:
    vertex_to_subtree_size[v] = 0
    return
  size = len(graph[v])
  for child in graph[v]:
    if child not in vertex_to_subtree_size:
      dfs(graph, vertex_to_subtree_size, child)
    size += vertex_to_subtree_size[child]
  vertex_to_subtree_size[v] = size

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