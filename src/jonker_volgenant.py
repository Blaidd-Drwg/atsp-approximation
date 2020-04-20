import operator
from functools import reduce
import networkx as nx


def jonker_volgenant(g):
    asymm_node_pairs = [{u, v} for u, v in g.edges() if g[u][v]['weight'] != g[v][u]['weight']]
    asymm_nodes = reduce(operator.or_, asymm_node_pairs, set())
    symm_nodes = set(g) - asymm_nodes

    max_weight = max(data['weight'] for u, v, data in g.edges(data=True))
    big = len(g) * max_weight + 1  # a weight so big that not using a 0 weight edge is never worth it
    huge = len(g) * (big + max_weight) + 1  # a weight so huge that it's never used in a tour
    if huge > 1 << 30:
        raise Exception('Edge weight too big for Concorde, Jonker-Volgenant cannot be applied.')

    n = len(g)
    g_sym = nx.Graph()
    node_map = dict((node, i) for i, node in enumerate(g))
    def v_in(node): return node_map[node]
    def v_out(node): return node_map[node] + n
    def v_sym(node): return v_in(node)

    for node in g:
        g_sym.add_node(v_in(node))
    for node in asymm_nodes:
        g_sym.add_node(v_out(node))

    # TODO assumption: no node key is negative
    for node in asymm_nodes:
        g_sym.add_edge(v_in(node), v_out(node), weight=0)

    for u in asymm_nodes:
        for v in asymm_nodes:
            if u == v:
                continue
            weight = g[u][v]['weight'] + big
            g_sym.add_edge(v_out(u), v_in(v), weight=weight)
            g_sym.add_edge(v_out(u), v_out(v), weight=huge)
            g_sym.add_edge(v_in(u), v_in(v), weight=huge)

    for u in symm_nodes:
        for v in asymm_nodes:
            weight = g[u][v]['weight'] + big
            g_sym.add_edge(v_sym(u), v_in(v), weight=weight)
            g_sym.add_edge(v_out(v), v_sym(u), weight=weight)

    for u in symm_nodes:
        for v in symm_nodes:
            if u == v:
                continue
            weight = g[u][v]['weight'] + big
            g_sym.add_edge(v_sym(u), v_sym(v), weight=weight)

    return g_sym
