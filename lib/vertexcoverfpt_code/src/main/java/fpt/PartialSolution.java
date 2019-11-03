package fpt;

import com.google.common.graph.EndpointPair;
import com.google.common.graph.Graphs;
import com.google.common.graph.MutableGraph;

import java.util.*;
import java.util.stream.Collectors;

public class PartialSolution {
    private MutableGraph<Integer> g;
    private Collection<Integer> currentVC;

    public PartialSolution(MutableGraph<Integer> g, Collection<Integer> currentVC) {
        this.g = g;
        this.currentVC = currentVC;
    }

    public PartialSolution(MutableGraph<Integer> g) {
        this(g, new ArrayList<>());
    }

    public MutableGraph<Integer> getG() {
        return g;
    }

    public Collection<Integer> getCurrentVC() {
        return currentVC;
    }

    public boolean isVertexCover() {
        boolean oneNotCovered = g.edges().parallelStream()
                .anyMatch(e -> !isCovered(e));
        return !oneNotCovered;
    }

    private boolean isCovered(EndpointPair<Integer> e) {
        return currentVC.stream()
                .anyMatch(v -> e.nodeU().equals(v) || e.nodeV().equals(v));
    }

    public int getSize() {
        return currentVC.size();
    }

    public PartialSolution selectNode(int node) {
        if(!g.nodes().contains(node) || currentVC.contains(node))
            throw new RuntimeException("Can't add unknown / already added node");
        MutableGraph<Integer> gCopy = Graphs.copyOf(g);
        Set<Integer> neighbours = gCopy.adjacentNodes(node);
        // remove node
        gCopy.removeNode(node);
        // remove neighbours that now have deg==0
        neighbours.stream()
                .filter(neighbour -> gCopy.degree(neighbour)==0)
                .forEach(gCopy::removeNode);
        ArrayList<Integer> vcCopy = new ArrayList<>(this.getCurrentVC());
        vcCopy.add(node);
        return new PartialSolution(gCopy, vcCopy);
    }

    public PartialSolution selectNodes(Integer... nodes) {
        return selectNodes(Arrays.asList(nodes));
    }

    public PartialSolution selectNodes(Iterable<Integer> nodes) {
        for (Integer node : nodes)
            if(!g.nodes().contains(node) || currentVC.contains(node))
                throw new RuntimeException("Can't add unknown / already added node");

        MutableGraph<Integer> gCopy = Graphs.copyOf(g);
        ArrayList<Integer> vcCopy = new ArrayList<>(this.getCurrentVC());
        for (Integer node : nodes){
            gCopy.removeNode(node);
            vcCopy.add(node);
        }
        // delete nodes with deg 0
        List<Integer> degZero = gCopy.nodes().stream()
                .filter(node -> gCopy.degree(node) == 0)
                .collect(Collectors.toList());
        for (int node : degZero) {
            gCopy.removeNode(node);
        }
        return new PartialSolution(gCopy, vcCopy);
    }
}
