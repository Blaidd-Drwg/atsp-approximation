package fpt;

import com.google.common.graph.GraphBuilder;
import com.google.common.graph.MutableGraph;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.OpenOption;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class Main {

    public static void main(String[] args) {
        try {
            String outFile;
            VCSolver solver = null;
            String pathToGraph = args[0];
            outFile = args[1];
            solver = new AdvancedSolver(pathToGraph);
            System.out.println("Calculating vertex cover..");
            PartialSolution vertexCover = solver.getVC();
            System.out.println("Found VC with size: " + vertexCover.getCurrentVC().size());
            writeVCToFile(vertexCover, outFile);
        } catch (IOException | IndexOutOfBoundsException e) {
            handleError(e);
        }
    }

    private static void writeVCToFile(PartialSolution vertexCover, String outFile) throws IOException {
        try (BufferedWriter writer = Files.newBufferedWriter(Paths.get(outFile), StandardOpenOption.WRITE, StandardOpenOption.CREATE)) {
            writer.write(Integer.toString(vertexCover.getCurrentVC().size()));
            writer.newLine();
            for (Integer node : vertexCover.getCurrentVC()) {
                writer.write(node.toString());
                writer.newLine();
            }
            writer.flush();
        }
    }

    private static void handleError(Exception e) {
        System.out.println("Error, use graph file as first argument and output file as second argument");
        System.err.println(e);
        System.exit(1);
    }
}
