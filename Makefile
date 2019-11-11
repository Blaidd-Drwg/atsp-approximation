LEMON_DIR=vendor/lemon
LEMON_BUILD_DIR=$(LEMON_DIR)/build
LEMON_INSTALL_DIR=$(LEMON_BUILD_DIR)/install
CONCORDE_BIN=vendor/concorde
MSA_DIR=lib/msa
MSA_BIN=$(MSA_DIR)/msa_solver
MSA_SRC=$(MSA_DIR)/msa.cpp
TSPLIB_DIR=instances/tsplib
TSPLIB_FILES=$(patsubst %.gz,%,$(wildcard $(TSPLIB_DIR)/*.gz))

all: $(MSA_BIN) $(CONCORDE_BIN) python_deps $(TSPLIB_DIR)

$(MSA_BIN): $(MSA_SRC) $(LEMON_INSTALL_DIR)
	$(CXX) -O3 "$(MSA_SRC)" -o "$(MSA_BIN)" -I "$(LEMON_INSTALL_DIR)/include"

$(LEMON_INSTALL_DIR): $(LEMON_DIR)
	mkdir -p "$(LEMON_BUILD_DIR)"
	cd "$(LEMON_BUILD_DIR)" && \
		cmake -DCMAKE_INSTALL_PREFIX="$(CURDIR)/$(LEMON_INSTALL_DIR)" "$(CURDIR)/$(LEMON_DIR)" && \
		cmake --build . -- install

$(LEMON_DIR):
	wget -O- "http://lemon.cs.elte.hu/pub/sources/lemon-1.3.1.tar.gz" | tar xz
	mv "lemon-1.3.1" "$(LEMON_DIR)"

$(CONCORDE_BIN):
	wget -O- "http://www.math.uwaterloo.ca/tsp/concorde/downloads/codes/linux24/concorde.gz" \
		| gunzip \
		> "$(CONCORDE_BIN)"
	chmod u+x "$(CONCORDE_BIN)"

python_deps:
	@command -v poetry || (echo "Poetry not found. Please install Poetry by executing 'python3 -m pip install poetry --user', then run Make again."; exit 1)
	poetry install

$(TSPLIB_DIR):
	mkdir -p "$(TSPLIB_DIR)"
	wget -O- "http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/atsp/ALL_atsp.tar" \
		| tar x -C "$(TSPLIB_DIR)"
	$(MAKE) unzip_tsplib

unzip_tsplib: $(TSPLIB_FILES)

$(TSPLIB_DIR)/%:
	gunzip $@.gz

test:
	poetry run python3 src/main.py -t instances/tsplib/ftv33.atsp --multibeta
	poetry run python3 src/main.py -c instances/tsplib/ftv33.atsp --multibeta

clean:
	rm -rf "$(LEMON_DIR)"
	rm -f "$(CONCORDE_BIN)"
	rm -f "$(MSA_BIN)"
	rm -rf "$(TSPLIB_DIR)"

.PHONY: all python_deps unzip_tsplib test clean
