import networkx as nx
import numpy as np


def to_graph(matrix, using=nx.DiGraph):
    copy = np.copy(matrix)
    copy[copy == 0] = -1
    g = nx.from_numpy_matrix(copy, create_using=using())
    for u, v, data in g.edges(data=True):
        if data['weight'] == -1:
            g[u][v]['weight'] = 0
    return g


def to_matrix(g):
    copy = g.copy()
    for u, v, data in copy.edges(data=True):
        if data['weight'] == 0:
            copy[u][v]['weight'] = -1
    matrix = nx.convert_matrix.to_numpy_array(copy)
    matrix[matrix == -1] = 0
    return matrix


def tour_cost(tour, g):
    return sum(g[u][v]['weight'] for u, v in zip(tour, tour[1:] + tour[:1]))


def metric_shortcut(tour):
    return list(dict.fromkeys(tour))


def rotate(l, n):
    return l[n:] + l[:n]
