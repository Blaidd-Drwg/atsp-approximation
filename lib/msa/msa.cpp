#include <iostream>
#include <fstream>
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

    int startNode = atoi(argv[1]);
    int dim;
    input >> dim;

    FullDigraph g(dim);
    FullDigraph::ArcMap<int> costs(g);

    int weight;
    for (int i = 0; i < dim; i++) {
        FullDigraph::Node u = g(i);
        for (int j = 0; j < dim; j++) {
            FullDigraph::Node v = g(j);
            input >> weight;
            costs[g.arc(u, v)] = weight;
        }
    }

    MinCostArborescence<FullDigraph, FullDigraph::ArcMap<int>> algo(g, costs);
    algo.run(g(startNode));

    std::ofstream output;
    output.open(argv[3]);

    for (int i = 0; i < dim; i++) {
        FullDigraph::Node u = g(i);
        for (int j = 0; j < dim; j++) {
            FullDigraph::Node v = g(j);
            bool inArbo = algo.arborescence(g.arc(u, v));
            output << static_cast<int>(inArbo);
        }
    }
    output << std::endl;
}
