import subprocess
import os
import pathlib
import tempfile
import networkx as nx


def vertex_cover(g):
    GRAPH_NAME = 'tmp.graph'
    OUT_NAME = 'tmp.vc'

    if not g.nodes:
        return set()
    g.remove_edges_from(nx.selfloop_edges(g))

    with tempfile.TemporaryDirectory() as tmpdir:
        graph_file = os.path.join(tmpdir, GRAPH_NAME)
        out_file = os.path.join(tmpdir, OUT_NAME)
        write_graph(g, graph_file)
        run_java(graph_file, out_file)
        return parse(out_file)


def run_java(graph_file, out_file):
    jar_path = pathlib.Path(__file__).parent.parent.joinpath('lib', 'vertexcoverfpt-jar-with-dependencies.jar')
    subprocess.run(['java', '-jar', jar_path, graph_file, out_file], stdout=subprocess.DEVNULL)


def parse(filename):
    with open(filename) as f:
        next(f)  # skip dimension line
        solution = ' '.join(f.readlines())
    return set(int(i) for i in solution.split())


def write_graph(g, filename):
    with open(filename, 'w') as f:
        f.write(f'{len(g)} {len(g.edges())}\n')
        for u, v in g.edges():
            f.write(f'{u} {v}\n')
