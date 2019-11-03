import csv
import sys
import math
import numpy as np


def parse_csv(filename):
    with open(filename) as f:
        matrix = []
        for line in csv.reader(f):
            row = [int(x) if x.strip() else math.inf for x in line]
            matrix.append(row)
    return np.asarray(matrix)


def parse_atsp(filename):
    with open(filename) as f:
        while True:
            line = f.readline().strip()
            if line.startswith("DIMENSION"):
                dim = int(line.split()[1])
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                assert(line.endswith("EXPLICIT"))
            elif line.startswith("EDGE_WEIGHT_FORMAT"):
                assert(line.endswith("FULL_MATRIX"))
            elif line.startswith("EDGE_WEIGHT_SECTION"):
                matrix_string = ' '.join([line.strip() for line in f])
                matrix_data = [int(i) for i in matrix_string.split() if i != "EOF"]
                return np.reshape(matrix_data, (dim, dim))


def parse_plain(filename):
    with open(filename) as f:
        dim = int(f.readline().strip())
        content = ' '.join(line.strip() for line in f)
        weights = [int(w) for w in content.split()[:dim**2]]
        return np.reshape(weights, (dim, dim))


def parse(filename, file_format=None):
    if not file_format:
        # guess format from file ending
        if filename.endswith('.atsp'):
            file_format = 'atsp'
        elif filename.endswith('.csv'):
            file_format = 'csv'
        elif filename[-2].isnumeric():
            file_format = 'plain'

    if file_format == "csv":
        return parse_csv(filename)
    elif file_format == "atsp":
        return parse_atsp(filename)
    elif file_format == 'plain':
        return parse_plain(filename)
    else:
        print("Format not recognized, only CSV, ATSP or plain files are supported")
        exit(1)


if __name__ == '__main__':
    print(parse(sys.argv[0]))
