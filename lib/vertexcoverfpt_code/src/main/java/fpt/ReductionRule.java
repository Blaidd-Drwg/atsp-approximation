package fpt;

import java.util.List;

public interface ReductionRule {

    /**
     * Takes an input problem and generates smaller problems
     * @param input a problem instance with already added vertices
     * @return multiple solutions, empty collection iff rule not applicable
     */
    List<PartialSolution> apply(PartialSolution input);
}
