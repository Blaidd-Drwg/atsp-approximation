import itertools
from scipy.special import comb


def check_metric(matrix):
    dimension = matrix.shape[0]
    metric = 0
    for i in range(dimension):
        for j in range(dimension):
            for k in range(dimension):
                if i == j or j == k or k == i:
                    continue

                if matrix[i, k] <= matrix[i, j] + matrix[j, k]:
                    metric += 1
    max_metric = dimension**3 - 3 * dimension**2 + 2 * dimension
    print(f'metric triangles: {metric}/{max_metric} ({round(100 * metric / max_metric)}%)')


def check_symmetry(matrix):
    facs = asymmetry_factors(matrix)

    n = matrix.shape[0]
    max_symmetric = int(comb(n, 2))
    symm = max_symmetric - len(facs)
    print(f'symmetric edges: {symm}/{max_symmetric} ({round(100 * symm / max_symmetric)}%)')
    facs = sorted(facs)
    print(f'max symmetry violation: {facs[-1] if facs else "None"}')
    print(f'median symmetry violation: {facs[len(facs)//2] if facs else "None"}')


def asymmetry_factors(matrix):
    n = matrix.shape[0]
    symm = 0
    facs = []
    for i, j in itertools.combinations(range(n), 2):
        if i == j:
            continue

        if matrix[i, j] == matrix[j, i]:
            symm += 1
        elif matrix[i, j] == 0:
            facs.append(matrix[j, i] / 0.1)
        elif matrix[j, i] == 0:
            facs.append(matrix[i, j] / 0.1)
        else:
            fac = matrix[i, j] / matrix[j, i]
            if fac < 1:
                fac = 1 / fac
            facs.append(fac)
    return facs


if __name__ == '__main__':
    import sys
    from parser import parse

    matrix = parse(sys.argv[1])
    check_metric(matrix)
    check_symmetry(matrix)
