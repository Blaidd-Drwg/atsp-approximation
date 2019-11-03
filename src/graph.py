from copy import deepcopy
import itertools
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


def metricize_cost_matrix(matrix):
    n = matrix.shape[0]
    np.fill_diagonal(matrix, 0)
    no_edge = np.max(matrix) + 1
    matrix[matrix == -1] = no_edge
    assert((matrix >= 0).all())

    for k in range(n):
        for i in range(n):
            for j in range(n):
                longcut = matrix[i][k] + matrix[k][j]
                if longcut < matrix[i][j]:
                    matrix[i][j] = longcut
    assert((matrix < no_edge).all())  # otherwise, the original graph isn't strongly connected
    return matrix


# force_symmetry does not determine the exact percentage of symmetric edges:
# maybe some edges were randomly chosen as symmetric,
# maybe metricizing the graph will make some edges asymmetric again
def generate_cost_matrix(n, force_symmetry=0.0):
    min_weight = 1
    max_weight = 100
    matrix = np.random.randint(min_weight, max_weight, size=(n, n))

    node_pairs = list(itertools.combinations(range(n), 2))
    symmetric_pairs = round(force_symmetry * len(node_pairs))
    random.shuffle(node_pairs)
    for u, v in node_pairs[:symmetric_pairs]:
        matrix[u][v] = matrix[v][u]
    return matrix


def generate_oneway_matrix(n, oneways=0.0):
    min_weight = 1
    max_weight = 100
    matrix = np.random.randint(min_weight, max_weight, size=(n, n))
    for u in range(n):
        for v in range(0, u):
            matrix[u][v] = matrix[v][u]

    num_oneways = round(oneways * n*(n-1))

    node_pairs = list(itertools.combinations(range(n), 2))
    random.shuffle(node_pairs)
    for u, v in node_pairs[:num_oneways]:
        # TOOD this should take care that the graph is still strongly connected,
        #      but this approach seems not really useful for us anyway
        matrix[u][v] = n * max_weight
    return matrix


def plot(g):
    pos = nx.circular_layout(g)
    nx.draw(g, pos)
    labels = nx.get_edge_attributes(g, 'weight')
    a_labels = {k: v for k, v in labels.items() if k[0] > k[1]}
    b_labels = {k: v for k, v in labels.items() if k[0] < k[1]}
    up_pos = deepcopy(pos)
    for v in up_pos.values():
        v[1] += 0.1
    nx.draw_networkx_edge_labels(g, up_pos, edge_labels=a_labels)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=b_labels)
    plt.show()


def remove_dead_nodes(matrix):
    for i in reversed(range(matrix.shape[0])):
        no_out_edge = (matrix[i, :i] == -1).all() and (matrix[i, i+1:] == -1).all()
        no_in_edge = (matrix[:i, i] == -1).all() and (matrix[i+1:, i] == -1).all()
        if no_out_edge or no_in_edge:
            matrix = np.delete(matrix, i, axis=0)
            matrix = np.delete(matrix, i, axis=1)
    return matrix
