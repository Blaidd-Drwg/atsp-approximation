package fpt;

import com.google.common.graph.EndpointPair;
import com.google.common.graph.Graphs;
import com.google.common.graph.MutableGraph;

import java.io.IOException;
import java.util.*;

/**
 * Very simple solver that adds one of the two vertices of an edge
 */
public class SimpleSolver extends VCSolver {

    public SimpleSolver(MutableGraph<Integer> g) {
        super(g);
    }

    public SimpleSolver(String inputPath) throws IOException {
        super(inputPath);
    }

    @Override
    List<ReductionRule> initRules() {
        // implement basic binary decision for an edge
        return Collections.singletonList(input -> {
            MutableGraph<Integer> g = input.getG();
            EndpointPair<Integer> edge = g.edges().stream().findAny().orElseThrow(() -> new RuntimeException("No more edges"));
            // select U for first new solution
            PartialSolution solution1 = input.selectNode(edge.nodeU());
            // select V for second new solution
            PartialSolution solution2 = input.selectNode(edge.nodeV());

            return Arrays.asList(solution1, solution2);
        });
    }
}
