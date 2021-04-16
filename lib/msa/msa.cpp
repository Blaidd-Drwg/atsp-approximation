#include <iostream>
#include <fstream>
#include <lemon/full_graph.h>
#include <lemon/min_cost_arborescence.h>

using namespace lemon;
typedef unsigned long long ull;

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: ./msa start_node input_file output_file" << std::endl;
        exit(1);
    }

    std::ifstream input;
    input.open(argv[2]);

    std::istringstream startNodeParser(argv[1]);
    ull startNode;
    startNodeParser >> startNode;
    ull dim;
    input >> dim;

    FullDigraph g(dim);
    FullDigraph::ArcMap<ull> costs(g);

    ull weight;
    for (ull i = 0; i < dim; i++) {
        FullDigraph::Node u = g(i);
        for (ull j = 0; j < dim; j++) {
            FullDigraph::Node v = g(j);
            input >> weight;
            costs[g.arc(u, v)] = weight;
        }
    }

    MinCostArborescence<FullDigraph, FullDigraph::ArcMap<ull> > algo(g, costs);
    algo.run(g(startNode));

    std::ofstream output;
    output.open(argv[3]);

    for (ull i = 0; i < dim; i++) {
        FullDigraph::Node u = g(i);
        for (ull j = 0; j < dim; j++) {
            FullDigraph::Node v = g(j);
            bool inArbo = algo.arborescence(g.arc(u, v));
            output << static_cast<int>(inArbo);
        }
    }
    output << std::endl;
}
