from util import err_print
import csv
import sys
import math
from enum import Enum, auto
import numpy as np


class FileFormat(Enum):
    TSPLIB = auto()
    CSV = auto()
    TSV = auto()
    PLAIN = auto()


def parse(filename, file_format=None):
    if file_format and not isinstance(file_format, FileFormat):
        raise ValueError("file_format must be an instance of FileFormat")

    if not file_format:
        if filename.endswith('.atsp'):
            file_format = FileFormat.TSPLIB
        elif filename.endswith('.csv'):
            file_format = FileFormat.CSV
        elif filename.endswith('.tsv'):
            file_format = FileFormat.TSV
        elif filename.endswith('.txt'):
            file_format = FileFormat.PLAIN
        else:
            err_print("Error: File name extension not recognized, use the --help flag to see the supported formats")
            exit(1)

    if file_format == FileFormat.TSPLIB:
        flattened_weight_matrix, dimension = parse_tsplib(filename)
    elif file_format == FileFormat.CSV:
        flattened_weight_matrix, dimension = parse_csv(filename, delimiter=',')
    elif file_format == FileFormat.TSV:
        flattened_weight_matrix, dimension = parse_csv(filename, delimiter='\t')
    elif file_format == FileFormat.PLAIN:
        flattened_weight_matrix, dimension = parse_plain(filename)

    assert(len(flattened_weight_matrix) == dimension**2)

    # if we have floating point weights, scale them and represent them as ints, since Concorde cannot handle floats
    flattened_weight_matrix = [float(weight_string) for weight_string in flattened_weight_matrix]
    max_decimal_place_count = max(decimal_place_count(weight_string) for weight_string in flattened_weight_matrix)
    scaling_factor = 10**max_decimal_place_count
    if scaling_factor > 1:
        err_print(f'Warning: Concorde does not support floating point weights, scaling all weights by a factor of {scaling_factor}.')
        err_print(f'To get the correct tour cost, scale the output tour cost back by dividing by {scaling_factor}')
    flattened_weight_matrix = [int(round(weight * scaling_factor)) for weight in flattened_weight_matrix]

    return np.reshape(flattened_weight_matrix, (dimension, dimension))


# we cast to float and back to str to get a uniform string representation
def decimal_place_count(weight):
    weight_string = str(weight)
    decimal_pos = weight_string.find('.')
    if decimal_pos == -1:
        return 0
    # if weight is an integer represented as float, e.g. '3.0'
    elif decimal_pos == len(weight_string) - 2 and weight_string[-1] == '0':
        return 0
    else:
        return len(weight_string) - (decimal_pos + 1)


def parse_csv(filename, **kwargs):
    with open(filename) as f:
        flattened_weight_matrix = []
        dimension = 0
        for row in csv.reader(f, **kwargs):
            flattened_weight_matrix += [x.strip() for x in row]
            dimension += 1
    return (flattened_weight_matrix, dimension)


def parse_tsplib(filename):
    with open(filename) as f:
        while True:
            line = f.readline().strip()
            if line.startswith("DIMENSION"):
                dimension = int(line.split()[1])
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                assert(line.endswith("EXPLICIT"))
            elif line.startswith("EDGE_WEIGHT_FORMAT"):
                assert(line.endswith("FULL_MATRIX"))
            elif line.startswith("EDGE_WEIGHT_SECTION"):
                data_lines = [line.strip() for line in f]  # consume the rest of the file
                data_string = ' '.join(data_lines)  # line breaks have no semantics
                flattened_weight_matrix = [weight_string for weight_string in data_string.split() if weight_string != "EOF"]
                return (flattened_weight_matrix, dimension)


def parse_plain(filename):
    with open(filename) as f:
        dimension = int(f.readline().strip())
        matrix_string = ' '.join(line.strip() for line in f)
        flattened_weight_matrix = matrix_string.split()[:dimension**2]
        return (flattened_weight_matrix, dimension)


if __name__ == '__main__':
    print(parse(sys.argv[0]))
