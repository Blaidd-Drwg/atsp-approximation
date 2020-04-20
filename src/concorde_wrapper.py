import subprocess
import os
import pathlib
import tempfile
from operator import itemgetter

from util import tour_cost
from jonker_volgenant import jonker_volgenant
from held_karp import held_karp


# g must be symmetric
def concorde_sym(g):
    TSP_NAME = 'tmp.tsp'
    OUT_NAME = 'tmp.sol'

    with tempfile.TemporaryDirectory() as tmpdir:
        tsp_file = os.path.join(tmpdir, TSP_NAME)
        out_file = os.path.join(tmpdir, OUT_NAME)
        write_tsplib(g, tsp_file)
        run_concorde(tsp_file, out_file)
        tour = parse(out_file)
    tour = [list(g.nodes)[i] for i in tour]
    return {'cost': tour_cost(tour, g), 'tour': tour}


def concorde_asym(g):
    g_sym = jonker_volgenant(g)

    # Concorde uses Held-Karp internally if n < 10
    # Its HK implementation cannot handle edge weights over 1 << 15, in that case use our own implementation
    if len(g_sym) < 10 and any(data['weight'] > (1 << 15) for u, v, data in g_sym.edges(data=True)):
        return held_karp(g)

    tour = concorde_sym(g_sym)['tour']
    tour = [list(g.nodes)[i] for i in tour if i < len(g)]
    rev_tour = tour[::-1]
    return min(
        {'cost': tour_cost(tour, g), 'tour': tour},
        {'cost': tour_cost(rev_tour, g), 'tour': rev_tour},
        key=itemgetter('cost'))


def run_concorde(tsp_file, out_file):
    # Concorde has tons of weird error messages, but it usually still works.
    # To reduce clutter, redirect stderr to /dev/null
    concorde_path = pathlib.Path(__file__).parent.parent.joinpath('vendor', 'concorde')
    subprocess.run([concorde_path, '-x', '-s0', '-o', out_file, tsp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def parse(filename):
    with open(filename) as f:
        next(f)  # skip dimension line
        solution = ' '.join(f.readlines())
    return [int(i) for i in solution.split()]


def write_tsplib(g, filename):
    with open(filename, 'w') as f:
        f.write(f'DIMENSION: {len(g)}\n')
        f.write('EDGE_WEIGHT_TYPE: EXPLICIT\n')
        f.write('EDGE_WEIGHT_FORMAT: FULL_MATRIX\n')
        f.write('EDGE_WEIGHT_SECTION\n')
        for u in g:
            for v in g:
                weight = g[u][v]['weight'] if u != v else 0
                f.write(str(weight))
                f.write(' ')
            f.write('\n')
