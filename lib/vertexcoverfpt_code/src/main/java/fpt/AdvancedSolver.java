package fpt;

import com.google.common.collect.Iterables;
import com.google.common.graph.MutableGraph;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

public class AdvancedSolver extends VCSolver {

    public AdvancedSolver(MutableGraph<Integer> g) {
        super(g);
    }

    public AdvancedSolver(String inputPath) throws IOException {
        super(inputPath);
    }

    @Override
    List<ReductionRule> initRules() {
        return Arrays.asList(
                AdvancedSolver::degOne,
                AdvancedSolver::degTwo,
                AdvancedSolver::degThree,
                AdvancedSolver::degFive,
                AdvancedSolver::allDegFour
        );
    }

    private static List<PartialSolution> degOne(PartialSolution input) {
        MutableGraph<Integer> g = input.getG();
        // check if there is node with deg==1 and select its neighbour
        Optional<Integer> maybeDegOne = g.nodes().stream()
                .filter(node -> g.degree(node) == 1)
                .map(node -> Iterables.getOnlyElement(g.adjacentNodes(node)))
                .findAny();
        List<PartialSolution> result;
        if (maybeDegOne.isPresent()) {
            PartialSolution reducedSolution = input.selectNode(maybeDegOne.get());
            result = Collections.singletonList(reducedSolution);
        } else {
            result = Collections.emptyList();
        }
        return result;
    }

    private static List<PartialSolution> degTwo(PartialSolution input) {
        MutableGraph<Integer> g = input.getG();
        // look for node with deg==2
        Optional<Integer> maybeDegTwo = g.nodes().stream()
                .filter(node -> g.degree(node) == 2)
                .findAny();
        List<PartialSolution> result;
        if (maybeDegTwo.isPresent()) {
            Integer degTwo = maybeDegTwo.get();
            Integer[] neighbours = g.adjacentNodes(degTwo).toArray(new Integer[2]);
            int a = neighbours[0];
            int b = neighbours[1];
            // cases: a and b connected, |N(a)∪N(b)|>2, |N(a)∪N(b)|=2
            if (g.hasEdgeConnecting(a, b)) { // case 1
                result = Collections.singletonList(input.selectNodes(a, b));
            } else {
                result = degTwoCase2or3(input, g, a, b);
            }
        } else {
            result = Collections.emptyList();
        }
        return result;
    }

    private static List<PartialSolution> degTwoCase2or3(PartialSolution input, MutableGraph<Integer> g, int a, int b) {
        List<PartialSolution> result;
        HashSet<Integer> abNeighbours = new HashSet<>();
        abNeighbours.addAll(g.adjacentNodes(a));
        abNeighbours.addAll(g.adjacentNodes(b));
        if (abNeighbours.size() > 2) { // case 2
            // choose {a,b} or N(a)∪N(b)
            PartialSolution abSolution = input.selectNodes(a, b);
            PartialSolution neighbourSolution = input.selectNodes(abNeighbours);
            result = Arrays.asList(abSolution, neighbourSolution);
        } else { // case 3 (
            result = Collections.singletonList(input.selectNodes(abNeighbours));
        }
        return result;
    }

    private static List<PartialSolution> degThree(PartialSolution input) {
        MutableGraph<Integer> g = input.getG();
        // look for node with deg==3
        Optional<Integer> maybeDegThree = g.nodes().stream()
                .filter(node -> g.degree(node) == 3)
                .findAny();
        List<PartialSolution> result;
        if (maybeDegThree.isPresent()) {
            Integer degThree = maybeDegThree.get();
            // try to apply different cases, result is empty list if not applicable
            result = degThreeCase1(g, input, degThree);
            if (result.isEmpty()) {
                result = degThreeCase2(g, input, degThree);
            }
            if (result.isEmpty()) {
                result = degThreeCase3(g, input, degThree);
            }
        } else {
            result = Collections.emptyList();
        }
        return result;
    }

    private static List<PartialSolution> degThreeCase1(MutableGraph<Integer> g, PartialSolution input, int degThree) {
        List<PartialSolution> result;
        Integer[] neighbours = g.adjacentNodes(degThree).toArray(new Integer[3]);
        int a = neighbours[0];
        int b = neighbours[1];
        int c = neighbours[2];
        Set<Integer> na = g.adjacentNodes(a);
        Set<Integer> nb = g.adjacentNodes(b);
        Set<Integer> nc = g.adjacentNodes(c);
        boolean disjoint = na.stream()
                .filter(nb::contains)
                .filter(nc::contains)
                .count() == 1; // only one common node (degThree)
        disjoint = disjoint && !g.hasEdgeConnecting(a, b);
        disjoint = disjoint && !g.hasEdgeConnecting(a, c);
        disjoint = disjoint && !g.hasEdgeConnecting(b, c);
        if (disjoint) { // case 1
            PartialSolution variant1 = input.selectNodes(na);
            PartialSolution variant2 = input.selectNodes(a, b, c);
            HashSet<Integer> thirdNodeSet = new HashSet<>();
            thirdNodeSet.add(a);
            thirdNodeSet.addAll(nb);
            thirdNodeSet.addAll(nc);
            PartialSolution variant3 = input.selectNodes(thirdNodeSet);
            result = Arrays.asList(variant1, variant2, variant3);
        } else { // not case 1
            result = Collections.emptyList();
        }
        return result;
    }

    private static List<PartialSolution> degThreeCase2(MutableGraph<Integer> g, PartialSolution input, int degThree) {
        List<PartialSolution> result;
        Integer[] neighbours = g.adjacentNodes(degThree).toArray(new Integer[3]);
        int a = neighbours[0];
        int b = neighbours[1];
        int c = neighbours[2];
        PartialSolution variant1 = null;
        PartialSolution variant2 = null;
        if (g.hasEdgeConnecting(a, b)) {
            variant1 = input.selectNodes(a, b, c);
            variant2 = input.selectNodes(g.adjacentNodes(c));
        } else if (g.hasEdgeConnecting(b, c)) {
            variant1 = input.selectNodes(a, b, c);
            variant2 = input.selectNodes(g.adjacentNodes(a));
        } else if (g.hasEdgeConnecting(a, c)) {
            variant1 = input.selectNodes(a, b, c);
            variant2 = input.selectNodes(g.adjacentNodes(b));
        }
        // iff there is an edge, variant1 was assigned to non null value
        if (variant1 != null) { // case 2
            result = Arrays.asList(variant1, variant2);
        } else { // not case 2
            result = Collections.emptyList();
        }
        return result;
    }

    private static List<PartialSolution> degThreeCase3(MutableGraph<Integer> g, PartialSolution input, int degThree) {
        Integer[] neighbours = g.adjacentNodes(degThree).toArray(new Integer[3]);
        int a = neighbours[0];
        int b = neighbours[1];
        int c = neighbours[2];
        List<Integer> common = commonNeighbours(g, a, b, degThree);
        if (common.size() == 0)
            common = commonNeighbours(g, a, c, degThree);
        if (common.size() == 0)
            common = commonNeighbours(g, b, c, degThree);
        PartialSolution variant1 = input.selectNodes(degThree, common.get(0));
        PartialSolution variant2 = input.selectNodes(a, b, c);
        return Arrays.asList(variant1, variant2);
    }

    private static List<Integer> commonNeighbours(MutableGraph<Integer> g, int a, int b, int v) {
        return g.adjacentNodes(a).stream()
                .filter(node -> g.hasEdgeConnecting(b, node)) // nodes adjacent to a and b
                .filter(node -> !node.equals(v))
                .collect(Collectors.toList());
    }

    private static List<PartialSolution> degFive(PartialSolution input) {
        MutableGraph<Integer> g = input.getG();
        // look for node with deg>=5
        Optional<Integer> maybeDegHigh = g.nodes().stream()
                .filter(node -> g.degree(node) > 4)
                .findAny();
        List<PartialSolution> result;
        if (maybeDegHigh.isPresent()) {
            Integer degHigh = maybeDegHigh.get();
            PartialSolution variant1 = input.selectNode(degHigh);
            PartialSolution variant2 = input.selectNodes(g.adjacentNodes(degHigh));
            result = Arrays.asList(variant1, variant2);
        } else {
            result = Collections.emptyList();
        }
        return result;
    }

    private static List<PartialSolution> allDegFour(PartialSolution input) {
        MutableGraph<Integer> g = input.getG();
        Optional<Integer> null_deg = g.nodes().stream().filter(node -> g.degree(node) == 0).findAny();
        while (null_deg.isPresent()) {
            int null_deg_node = null_deg.get();
            g.removeNode(null_deg_node);
            null_deg = g.nodes().stream().filter(node -> g.degree(node) == 0).findAny();
        }
        if (g.nodes().stream().anyMatch(node -> g.degree(node) != 4)) {
            throw new RuntimeException("Not only nodes with degree 4");
        }
        int node = g.nodes().iterator().next();
        PartialSolution variant1 = input.selectNode(node);
        PartialSolution variant2 = input.selectNodes(g.adjacentNodes(node));

        return Arrays.asList(variant1, variant2);
    }
}
