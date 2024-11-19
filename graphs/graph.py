from collections import defaultdict

def create_graph(edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)  # If the graph is undirected, include this line. Omit if it's directed.
    return graph