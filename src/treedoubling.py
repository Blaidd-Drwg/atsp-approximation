import math
import networkx as nx
import itertools
from networkx.algorithms.components import weakly_connected_components
from networkx.utils import pairwise
from networkx.algorithms.euler import eulerian_circuit

from held_karp import held_karp
from util import tour_cost, metric_shortcut
from msa_wrapper import calc_msa


# exact_algo must be a callable with signature: DiGraph -> {'cost': int, 'tour': [int]}
def g_treedoubling(g, exact_algo=held_karp, beta=1.0):
    # 1. Dividing the graph into components
    best_msa = None
    best_k = len(g)
    for start_node in g:
        msa = calc_msa(g, start_node)
        one_way_edge_count = len(list(find_one_way_edges(msa.edges, g, beta)))
        if one_way_edge_count < best_k:
            best_msa = msa
            best_k = one_way_edge_count
    msa = best_msa
    one_way_edges = list(find_one_way_edges(msa.edges, g, beta))

    # degenerate case: no one-way edges in msa => just do tree doubling
    if not one_way_edges:
        start_node = next(iter(g.nodes))
        tour = component_path(msa, g.nodes, start_node, start_node)
        tour = metric_shortcut(tour)
        return {'cost': tour_cost(tour, g), 'tour': tour, 'kernel_size': 0}

    for u, v in one_way_edges:
        msa.remove_edge(u, v)

    components = list(weakly_connected_components(msa))

    # 2. Finding a tour of the components
    meta_graph = nx.DiGraph()
    for (c1, nodes_1), (c2, nodes_2) in itertools.permutations(enumerate(components), 2):
        min_edge = cheapest_edge_between(nodes_1, nodes_2, g)
        # preserve a reference to the original edge
        u, v = min_edge
        meta_graph.add_edge(c1, c2, weight=g[u][v]['weight'], original=min_edge)

    meta_tour = exact_algo(meta_graph)['tour']
    in_nodes, out_nodes = get_in_and_out_nodes(meta_tour, meta_graph)

    # 3. Finding a Hamilton path for each component
    eulerian_trails = [component_path(msa, comp_nodes, in_node, out_node)
                       for comp_nodes, in_node, out_node
                       in zip(components, in_nodes, out_nodes)]

    # 4. Combining the component tour with the paths
    tour = []
    for comp_index in meta_tour:
        tour += eulerian_trails[comp_index]
    tour = metric_shortcut(tour)
    return {'cost': tour_cost(tour, g), 'tour': tour, 'kernel_size': len(one_way_edges)}


def find_one_way_edges(edges, g, beta):
    for u, v in edges:
        uvweight = max(g[u][v]['weight'], 0.1)
        if beta * uvweight < g[v][u]['weight']:
            yield u, v


def cheapest_edge_between(nodes_1, nodes_2, g):
    min_edge = None
    min_weight = math.inf
    for u in nodes_1:
        for v in nodes_2:
            if g[u][v]['weight'] < min_weight:
                min_edge = (u, v)
                min_weight = g[u][v]['weight']
    return min_edge


def get_in_and_out_nodes(meta_tour, meta_graph):
    in_nodes = [None] * len(meta_tour)
    out_nodes = [None] * len(meta_tour)

    for c1, c2 in zip(meta_tour, meta_tour[1:] + meta_tour[:1]):
        u, v = meta_graph[c1][c2]['original']
        out_nodes[c1] = u
        in_nodes[c2] = v
    return in_nodes, out_nodes


def component_path(msa, comp_nodes, in_node, out_node):
    # degenerate case in which the Eulerian path is empty
    if len(comp_nodes) == 1:
        return comp_nodes

    comp_graph = msa.subgraph(comp_nodes).copy()
    # tree doubling
    for u, v, attrs in comp_graph.edges(data=True):
        comp_graph.add_edge(v, u, **attrs)

    # remove the path from v_out to v_in
    if in_node != out_node:
        path = next(nx.all_simple_paths(comp_graph, out_node, in_node))
        for u, v in pairwise(path):
            comp_graph.remove_edge(u, v)

        # networkx cannot compute Eulerian trails, only circuits (yet)
        # => add dummy edge from v_out to v_in to close the circuit
        comp_graph.add_edge(out_node, in_node)

    eulerian_edges = eulerian_circuit(comp_graph, source=in_node)
    # the last node is the first, so it is intentionally ignored
    return [u for u, v in eulerian_edges]
