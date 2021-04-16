import argparse
import random
import sys

import parser
from treedoubling import g_treedoubling
from check_symmetry_metric import check_symmetry, asymmetry_factors
from concorde_wrapper import concorde_asym
from christofides import g_christofides
from graph import generate_cost_matrix, generate_oneway_matrix, metricize_cost_matrix, remove_dead_nodes
from held_karp import held_karp
from util import to_graph, tour_cost
from vc_wrapper import vertex_cover


# useful as benchmark
def random_tour(g):
    tour = list(g)
    random.shuffle(tour)
    return {'cost': tour_cost(tour, g), 'tour': tour}


def multibeta(matrix, algo, compute_tour, output_tour):
    g = to_graph(matrix)
    # plot(g)

    if compute_tour:
        exact_algo = concorde_asym
    else:
        # skip the (possibly expensive) exact computation by returning a dummy tour
        exact_algo = lambda graph: {'cost': 0, 'tour': list(graph)}

    #  run(g, algo, 0, compute_tour, output_tour)
    print(format_output({**exact_algo(g), 'kernel_size': len(g)}, 0, compute_tour, output_tour))  # exact solution

    facs = sorted(asymmetry_factors(matrix), reverse=True)
    asym_ratio = 1  # start using all asymmetric edges
    while True:
        beta_index = round(asym_ratio * len(facs))
        if beta_index >= len(facs):
            beta = 1
        else:
            beta = facs[int(beta_index)]

        run(g, algo, beta, compute_tour, output_tour)

        if round(asym_ratio * len(facs)) > 0:
            asym_ratio /= 2
        else:
            break


def run(g, algo, beta, compute_tour, output_tour):
    if compute_tour:
        exact_algo = concorde_asym
    else:
        # skip the expensive exact computation by returning a dummy tour
        exact_algo = lambda graph: {'cost': 0, 'tour': list(graph)}

    if algo == 'treedoubling':
        solution = g_treedoubling(g, exact_algo=exact_algo, beta=beta)
    elif algo == 'christofides':
        solution = g_christofides(g, exact_algo=exact_algo, vc_algo=vertex_cover, beta=beta)
    else:
        raise ValueError(f'invalid algo: {algo}')
    print(format_output(solution, beta, compute_tour, output_tour))


def compare_algos(matrix):
    g = to_graph(matrix)
    print(f'generalized treedoubling (concorde): {g_treedoubling(g, exact_algo=concorde_asym)}')
    print(f'generalized christofides (concorde): {g_christofides(g, exact_algo=concorde_asym, vc_algo=vertex_cover)}')
    print(f'concorde: {concorde_asym(g)}')
    print(f'held karp: {held_karp(g)}')
    print(f'random: {random_tour(g)}')


def format_output(solution, beta, compute_tour, output_tour):
    output = [str(n) for n in [beta, solution['kernel_size']]]
    if compute_tour:
        output.append(str(solution['cost']))
    if output_tour:
        output.append(' '.join(str(n) for n in solution['tour']))
    return ', '.join(output)


def main():
    # If you change the arguments or the help text, remember to update the README
    argparser = argparse.ArgumentParser('', formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument('graph',
                           help='A file describing a graph. Multiple formats are supported, identified by the\n'
                           'file name extension:\n'
                           '  .atsp: TSPLIB files with EDGE_WEIGHT_FORMAT=FULL_MATRIX\n'
                           '  .csv: weight matrices in CSV format\n'
                           '  .tsv: weight matrices in TSV format\n'
                           "  .txt: the graph's dimension followed by whitespace-separated edge weights.")

    algo_group = argparser.add_mutually_exclusive_group(required=True)
    algo_group.add_argument('-t', '--treedoubling', dest='algo', action='store_const', const='treedoubling',
                            help='Use the generalized tree doubling algorithm')
    algo_group.add_argument('-c', '--christofides', dest='algo', action='store_const', const='christofides',
                            help='Use the generalized Christofides algorithm')

    result_group = argparser.add_mutually_exclusive_group(required=False)
    result_group.add_argument('--only-kernel-size', action='store_false', dest='compute_tour',
                           help="Only output the instance's kernel size without computing a tour")
    result_group.add_argument('--tour', action='store_true', dest='output_tour',
                           help='Output the computed tour as a space-separated node list')

    beta_group = argparser.add_mutually_exclusive_group(required=False)
    beta_group.add_argument('-b', '--beta', default=1, type=float,
                            help='Asymmetry factor above which edges are treated as asymmetric (default: %(default)d).\n'
                            'Choosing beta = 0 will compute an exact solution.')
    beta_group.add_argument('--multibeta', action='store_true',
                            help='Execute the script multiple times with different values for beta.\n'
                            'First, compute an exact solution as a reference point. After that, start\n'
                            'by treating every asymmetric edge as asymmetric (beta = 1), then halve\n'
                            'the number of asymmetric edges each time until no asymmetric edges remain.')

    if len(sys.argv) == 1:
        argparser.print_help()
        exit()

    args = argparser.parse_args()

    matrix = parser.parse(args.graph)
    # np.random.seed(0)
    # matrix = generate_cost_matrix(80, force_symmetry=0.5)
    # matrix = generate_oneway_matrix(80, oneways=0.1)

    matrix = remove_dead_nodes(matrix)  # useful if matrix comes from a Hamilton path instance
    matrix = metricize_cost_matrix(matrix)
    # check_symmetry(matrix)
    # compare_algos(matrix)
    g = to_graph(matrix)

    fields = ['beta', 'kernel_size']
    if args.compute_tour:
        fields.append('tour_cost')
    if args.output_tour:
        fields.append('tour')
    print(', '.join(fields))

    if args.multibeta:
        multibeta(matrix, args.algo, args.compute_tour, args.output_tour)
    else:
        g = to_graph(matrix)
        run(g, args.algo, args.beta, args.compute_tour, args.output_tour)


if __name__ == '__main__':
    main()
