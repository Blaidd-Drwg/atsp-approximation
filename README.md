# From Symmetry to Asymmetry: Generalizing TSP Approximations by Parametrization
[![Build Status](https://travis-ci.com/Blaidd-Drwg/atsp-approximation.svg?branch=master)](https://travis-ci.com/Blaidd-Drwg/atsp-approximation)

This repository provides a reference implementation of the algorithms presented in the paper ['From Symmetry to Asymmetry: Generalizing TSP Approximations by Parametrization'](https://arxiv.org/abs/1911.02453).

## Dependencies
Python >= 3.6 and Java >= 8 are required to run the program. The remaining dependencies can either be downloaded and built automatically by Make (Linux only), or manually. The build process requires a C++ compiler, CMake and Make.

### Makefile
Install Poetry, which will manage the Python dependencies:
```
$ python3 -m pip install poetry --user
```
Use Make to automatically download and build all dependencies:
```
$ make all
```

### Manual build
- Download [Concorde](http://www.math.uwaterloo.ca/tsp/concorde/downloads/downloads.htm) and save the binary under `vendor/concorde`.
- Either install the LEMON graph library via a package manager, or [build it from source](https://lemon.cs.elte.hu/trac/lemon/wiki/Downloads).
- Build the MSA solver by running `g++ -O3 lib/msa/msa.cpp -o lib/msa/msa_solver`. If you built LEMON from source, you will need to point g++ toward the LEMON headers via the `-I` flag.
- Install Poetry by running `python3 -m pip install poetry --user`. Poetry will manage the Python dependencies.
- Install the Python dependencies in a new virtual environment by running `poetry install`.
- Download the [TSPLIB ATSP instances](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/atsp/ALL_atsp.tar) and place them in the `instances/tsplib` directory.

## Running
Enter the virtual environment and execute the main script:
```
$ poetry shell
$ python3 src/main.py
```
The script supports the following arguments:
```
usage: [-h] (-t | -c) [--only-kernel-size | --tour] [-b BETA | --multibeta] graph

positional arguments:
  graph                 A file describing a graph. Multiple formats are supported, identified by the
                        file name extension:
                          .atsp: TSPLIB files with EDGE_WEIGHT_FORMAT=FULL_MATRIX
                          .csv: weight matrices in CSV format
                          .tsv: weight matrices in TSV format
                          .txt: the graph's dimension followed by whitespace-separated edge weights.

optional arguments:
  -h, --help            show this help message and exit
  -t, --treedoubling    Use the generalized tree doubling algorithm
  -c, --christofides    Use the generalized Christofides algorithm
  --only-kernel-size    Only output the instance's kernel size without computing a tour
  --tour                Output the computed tour as a space-separated node list
  -b BETA, --beta BETA  Asymmetry factor above which edges are treated as asymmetric (default: 1).
                        Choosing beta = 0 will compute an exact solution.
  --multibeta           Execute the script multiple times with different values for beta.
                        First, compute an exact solution as a reference point. After that, start
                        by treating every asymmetric edge as asymmetric (beta = 1), then halve
                        the number of asymmetric edges each time until no asymmetric edges remain.
```
