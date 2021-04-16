#include <iostream>
#include <fstream>
#include <cstdint>
#include <lemon/full_graph.h>
#include <lemon/min_cost_arborescence.h>

using namespace lemon;

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cerr << "Usage: ./msa start_node input_file output_file" << std::endl;
        exit(1);
    }

    std::ifstream input;
    input.open(argv[2]);

    std::istringstream startNodeParser(argv[1]);
    uint64_t startNode;
    startNodeParser >> startNode;
    uint64_t dim;
    input >> dim;

    FullDigraph g(dim);
    FullDigraph::ArcMap<uint64_t> costs(g);

    uint64_t weight;
    for (uint64_t i = 0; i < dim; i++) {
        FullDigraph::Node u = g(i);
        for (uint64_t j = 0; j < dim; j++) {
            FullDigraph::Node v = g(j);
            input >> weight;
            costs[g.arc(u, v)] = weight;
        }
    }

    MinCostArborescence<FullDigraph, FullDigraph::ArcMap<uint64_t> > algo(g, costs);
    algo.run(g(startNode));

    std::ofstream output;
    output.open(argv[3]);

    for (uint64_t i = 0; i < dim; i++) {
        FullDigraph::Node u = g(i);
        for (uint64_t j = 0; j < dim; j++) {
            FullDigraph::Node v = g(j);
            bool inArbo = algo.arborescence(g.arc(u, v));
            output << static_cast<int>(inArbo);
        }
    }
    output << std::endl;
}
