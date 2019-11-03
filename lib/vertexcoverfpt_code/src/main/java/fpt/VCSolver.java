package fpt;

import com.google.common.graph.GraphBuilder;
import com.google.common.graph.MutableGraph;

import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.LinkedList;
import java.util.List;
import java.util.stream.IntStream;

public abstract class VCSolver {
    private MutableGraph<Integer> g;
    private List<ReductionRule> reductionRules = initRules();

    // for calculation
    private int bestSize = Integer.MAX_VALUE;
    private PartialSolution bestSolution = null;

    public VCSolver(MutableGraph<Integer> g) {
        this.g = g;
    }

    public VCSolver(String inputPath) throws IOException {
        this.g = parseGraph(inputPath);
    }

    private MutableGraph<Integer> parseGraph(String inputPath) throws IOException { BufferedReader br = Files.newBufferedReader(Paths.get(inputPath)); String[] firstLine = br.readLine().split(" ");
        int n = Integer.parseInt(firstLine[0]);
        int m = Integer.parseInt(firstLine[1]);
        // build graph
        MutableGraph<Integer> g = GraphBuilder.undirected().expectedNodeCount(n).build();
        // add vertices
        IntStream.rangeClosed(1, n).boxed().forEach(g::addNode);
        // add edges
        br.lines().forEach(line -> {
            String[] splitted = line.split(" ");
            Integer v1 = Integer.parseInt(splitted[0]);
            Integer v2 = Integer.parseInt(splitted[1]);
            g.putEdge(v1, v2);
        });
        br.close();
        return g;
    }

    abstract List<ReductionRule> initRules();

    public PartialSolution getVC() {
        if (bestSolution == null)
            calcVC();
        return bestSolution;
    }

    /**
     * Calculates VC with O*(1.3^k) run time.
     * <p>
     * Branched/Reduced subsolutions are put into stack, to achieve a
     * DFS like behaviour, in order to not use too much memory
     * <p>
     * The solution is put into this.bestSolution
     */
    private void calcVC() {
        LinkedList<PartialSolution> solutions = new LinkedList<>();
        solutions.push(new PartialSolution(g));

        while (!solutions.isEmpty()) {
            PartialSolution current = solutions.pop();
            // apply first rule, which can be applied
            List<PartialSolution> children = Collections.emptyList();
            for (ReductionRule rule : reductionRules) {
                children = rule.apply(current);
                if (!children.isEmpty()) {
                    break; // stop after first rule that could be applied
                }
            }
            // check if any child is solution, otherwise put on stack
            for (PartialSolution child : children) {
                if (child.isVertexCover()) {
                    // update best solution, if necessary
                    int size = child.getSize();
                    if (size < bestSize) {
                        bestSize = size;
                        System.out.println("Current VC size: " + size);
                        bestSolution = child;
                    }
                } else {
                    // put new branch and reduce
                    solutions.push(child);
                }
            }
        }
    }
}
