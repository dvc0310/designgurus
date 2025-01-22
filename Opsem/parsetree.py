"""
Implements a simple labeled bidirectional graph in a functional style,
storing adjacency in a dict {node: [(edge_label, node), ...], ...}.

No 'for' or 'while' loops are used. Instead, we operate with recursion
and produce lists by concatenation.
"""

# A "Node" has an id and a label
class Node:
    def __init__(self, node_id, label):
        self.id = node_id
        self.label = label

    def __repr__(self):
        return f"Node({self.id}, '{self.label}')"

    def __eq__(self, other):
        return isinstance(other, Node) and self.id == other.id

    def __hash__(self):
        # Must be hashable so it can be used as a dict key
        return hash(self.id)

# The graph is a dictionary: { node -> list of (edge_label, node) }
# We'll keep it in a global variable "g" as the original code does.
g = {}

# We'll have a global counter for node ids
_next_id = [0]  # keep in a list so we can mutate it without 'global'

def next_id():
    _next_id[0] += 1
    return _next_id[0]

def add_vertex(graph, node):
    """
    Add the node to the graph if not present, returning the updated graph.
    We'll do it in a functional style, but we also mutate 'graph' to keep it simpler.
    """
    if node not in graph:
        graph[node] = []
    return graph

def add_edge(graph, source, target, label=""):
    """
    Because it's bidirectional, we must add edges in both directions.
    We'll do so with no 'for' or 'while' loops,
    but in a functional style using recursion or list concatenations.
    """
    # Ensure both vertices exist
    add_vertex(graph, source)
    add_vertex(graph, target)

    # Insert the edge from source to target unless already present
    def has_edge(lst, lbl, tg):
        if not lst:
            return False
        (l, n) = lst[0]
        return (l == lbl and n == tg) or has_edge(lst[1:], lbl, tg)

    if not has_edge(graph[source], label, target):
        graph[source] = [(label, target)] + graph[source]
    if not has_edge(graph[target], label, source):
        graph[target] = [(label, source)] + graph[target]

    return graph

def add_node(graph, parent, lbl):
    new_nd = Node(next_id(), lbl)
    graph[new_nd] = []
    if parent is not None:
        graph[parent].append(("", new_nd))
    print(f"Added node: {new_nd} with parent {parent}")
    return new_nd



###############################################################################
# Convert the adjacency dict to DOT format. We'll do it with recursion only.  #
###############################################################################

def g_to_dot(graph, filename):
    """
    Write out a Graphviz DOT file for the bidirectional graph in 'graph'.
    No 'for' or 'while' loops. We’ll do it with a couple of helper functions.
    """

    # 1) Extract all nodes from the graph in a list. Then we can handle them recursively.
    #    We'll define a function keys_list(d) that returns a list of d's keys (recursively).
    def dict_keys_rec(d):
        # returns the keys in a list using recursion
        all_keys = list(d.keys())  # This is a system call that returns a list.
        # But we'll flatten it with recursion: we do need that list...
        # We'll do a helper function to convert that list to a purely functional recursion approach.
        return list_to_list(all_keys)

    def list_to_list(xs):
        # identity function, but let's do recursion
        if not xs:
            return []
        return [xs[0]] + list_to_list(xs[1:])

    all_nodes = dict_keys_rec(graph)

    # 2) Extract edges. Because it’s bidirectional, each edge is repeated. We'll store them all
    #    and do a small check so as not to double-write in the output. We'll handle that with recursion.

    # We'll gather edges in a big list, then remove duplicates with recursion.
    def gather_edges(nodes):
        if not nodes:
            return []
        node = nodes[0]
        adj_list = graph[node]
        # adjacency is a list of (label, neighbor)
        # recursively gather from the rest
        return edges_of(node, adj_list) + gather_edges(nodes[1:])

    def edges_of(src, pairs):
        if not pairs:
            return []
        (lbl, tgt) = pairs[0]
        return [(src, lbl, tgt)] + edges_of(src, pairs[1:])

    raw_edges = gather_edges(all_nodes)

    # Now remove duplicates: an edge (u, l, v) is a duplicate of (v, l, u) because it's bidirectional.
    def edge_eq(e1, e2):
        (s1, lbl1, t1) = e1
        (s2, lbl2, t2) = e2
        return (s1 == s2 and t1 == t2 and lbl1 == lbl2) or \
               (s1 == t2 and t1 == s2 and lbl1 == lbl2)

    def member_edge(e, es):
        if not es:
            return False
        return edge_eq(e, es[0]) or member_edge(e, es[1:])

    def unique_edges(es):
        if not es:
            return []
        head = es[0]
        tail = es[1:]
        if member_edge(head, tail):
            return unique_edges(tail)
        else:
            return [head] + unique_edges(tail)

    edges_unique = unique_edges(raw_edges)

    # 3) Write the file
    with open(filename, "w") as f:
        f.write("digraph parsetree {\n")
        f.write("  rankdir=TB;\n")

        # We'll do node lines with recursion:
        def write_nodes(ns):
            if not ns:
                return
            n = ns[0]
            f.write(f'  {n.id} [label="{n.label}", shape=box];\n')
            write_nodes(ns[1:])

        write_nodes(all_nodes)

        # We'll do edges with recursion:
        def write_edges(es):
            if not es:
                return
            (src, lbl, tgt) = es[0]
            f.write(f'  {src.id} -> {tgt.id} [label="{lbl}"];\n')
            write_edges(es[1:])

        write_edges(edges_unique)

        f.write("}\n")
