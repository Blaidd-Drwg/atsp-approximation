import subprocess
import os
import pathlib
import tempfile
import networkx as nx


def calc_msa(g, start_node):
    GRAPH_NAME = 'tmp.graph'
    OUT_NAME = 'tmp.msa'

    if not g.nodes:
        return nx.DiGraph()

    with tempfile.TemporaryDirectory() as tmpdir:
        graph_file = os.path.join(tmpdir, GRAPH_NAME)
        out_file = os.path.join(tmpdir, OUT_NAME)
        write_graph(g, graph_file)
        run_msa(start_node, graph_file, out_file)
        return parse(out_file, g)


def run_msa(start_node, graph_file, out_file):
    solver_path = pathlib.Path(__file__).parent.parent.joinpath('lib', 'msa', 'msa_solver')
    subprocess.run([solver_path, str(start_node), graph_file, out_file])


def parse(filename, g):
    msa = nx.DiGraph()

    with open(filename) as f:
        bits = f.read().strip()
    it = iter(bits)
    for u in range(len(g)):
        for v in range(len(g)):
            if next(it) == '1':
                msa.add_edge(u, v, **g[u][v])
    return msa


def write_graph(g, filename):
    with open(filename, 'w') as f:
        f.write(str(len(g)))
        f.write('\n')
        for u in g:
            for v in g:
                weight = g[u][v]['weight']
                f.write(str(weight))
                f.write(' ')
            f.write('\n')
