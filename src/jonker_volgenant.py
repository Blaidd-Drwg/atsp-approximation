import networkx as nx


def jonker_volgenant(g):
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

    # TODO assumption: no node key is negative
    for node in g:
        g_sym.add_node(v_in(node))
        g_sym.add_node(v_out(node))
        g_sym.add_edge(v_in(node), v_out(node), weight=0)

    for u in g:
        for v in g:
            if u == v:
                continue
            weight = g[u][v]['weight'] + big
            g_sym.add_edge(v_out(u), v_in(v), weight=weight)
            g_sym.add_edge(v_out(u), v_out(v), weight=huge)
            g_sym.add_edge(v_in(u), v_in(v), weight=huge)

    return g_sym
