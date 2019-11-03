# From Symmetry to Asymmetry: Generalizing TSP Approximations by Parametrization

This repository provides a reference implementation of the algorithms presented in the paper ['From Symmetry to Asymmetry: Generalizing TSP Approximations by Parametrization'](TODO arxiv link).

## Dependencies
Python >= 3.6 and Java >= 8 are required to run the program. The remaining dependencies can either be downloaded and built automatically by Make (Linux only), or manually. The build process requires a C++ compiler, CMake and Make.

### Makefile
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
This will print a summary of the command line options.
