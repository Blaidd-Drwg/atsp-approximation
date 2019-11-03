import random
import networkx as nx
from networkx.algorithms.matching import max_weight_matching
from networkx.algorithms.tree import minimum_spanning_tree

from held_karp import held_karp
from util import tour_cost, metric_shortcut, rotate
from vertex_cover import vertex_cover

ZERO_EDGE_WEIGHT = 0.1  # weight to assign zero edges when computing the asymmetry factor


def find_aymm_edges(g, beta):
    asymm_edges = []
    for u, v in g.edges():
        uvweight = max(g[u][v]['weight'], ZERO_EDGE_WEIGHT)
        vuweight = max(g[v][u]['weight'], ZERO_EDGE_WEIGHT)
        if beta * uvweight < vuweight \
           or beta * vuweight < uvweight:
            asymm_edges.append((u, v))
    return asymm_edges


def g_christofides(g, exact_algo=held_karp, vc_algo=vertex_cover, beta=1.0):
    random.seed(0)
    asymm_edges = find_aymm_edges(g, beta)
    asymm_nodes = vc_algo(g.edge_subgraph(asymm_edges).to_undirected())
    symm_nodes = g.nodes() - asymm_nodes

    if len(symm_nodes) <= 1:
        return {**exact_algo(g), 'kernel_size': len(g)}
    elif len(asymm_nodes) <= 1:  # if the asymmetric tour is trivial, don't bother
        tour = christofides(g.to_undirected()) + list(asymm_nodes)
        tour = metric_shortcut(tour)
        return {'cost': tour_cost(tour, g), 'tour': tour, 'kernel_size': 0}

    double_node = random.choice(tuple(symm_nodes))
    asymm_nodes.add(double_node)

    asymm_tour = exact_algo(g.subgraph(asymm_nodes))['tour']
    undir_g = to_undirected(g.subgraph(symm_nodes))
    symm_tour = christofides(undir_g)
    rev_symm_tour = symm_tour[::-1]
    symm_tour = symm_tour if tour_cost(symm_tour, g) <= tour_cost(rev_symm_tour, g) else rev_symm_tour

    asymm_tour = rotate(asymm_tour, asymm_tour.index(double_node) + 1)  # double node at end
    symm_tour = rotate(symm_tour, symm_tour.index(double_node))  # double node at start
    tour = metric_shortcut(asymm_tour + symm_tour)

    return {'cost': tour_cost(tour, g), 'tour': tour, 'kernel_size': len(asymm_nodes)}


def to_undirected(g):
    undir_g = nx.Graph()
    for u in g:
        for v in g:
            weight = min(g[u][v]['weight'], g[v][u]['weight'])
            undir_g.add_edge(u, v, weight=weight)
    return undir_g


def christofides(g):
    mst = minimum_spanning_tree(g)

    odd_degree_nodes = [node for node, degree in mst.degree() if degree % 2 == 1]
    odd_subgraph = g.subgraph(odd_degree_nodes).copy()

    # invert weight since networkx can only do max weight matching
    for edge in odd_subgraph.edges(data=True):
        edge[2]['weight'] = -edge[2]['weight']
    matching = max_weight_matching(odd_subgraph, maxcardinality=True)

    eulerian_graph = nx.MultiGraph(mst)
    for u, v in matching:
        eulerian_graph.add_edge(u, v, **g[u][v])

    eulerian_edges = nx.eulerian_circuit(eulerian_graph)
    return [u for u, v in eulerian_edges]
