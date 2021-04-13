#!/bin/sh

# Test that the program's behavior is not modified so the results from the paper are reproducible
EXPECTED_TREEDOUBLING="beta, kernel_size, tour_cost
0, 34, 1286
1, 19, 1728
1.3084112149532712, 16, 1728
1.6, 16, 1728
1.9069767441860466, 14, 1728
2.375, 11, 1858
3.1372549019607847, 6, 1971
3.5625, 2, 1580
4.380952380952381, 1, 1594
4.642857142857143, 1, 1594
6.571428571428571, 0, 1928
6.571428571428571, 0, 1928
18.75, 0, 1680"
EXPECTED_CHRISTOFIDES="beta, kernel_size, tour_cost
0, 34, 1286
1, 29, 1443
1.3084112149532712, 23, 1652
1.6, 19, 1861
1.9069767441860466, 14, 2019
2.375, 11, 1844
3.1372549019607847, 9, 1936
3.5625, 5, 2009
4.380952380952381, 4, 2086
4.642857142857143, 3, 1954
6.571428571428571, 0, 1704
6.571428571428571, 0, 1704
18.75, 0, 1704"

echo -n "Testing generalized tree doubling algorithm... "
ACTUAL_TREEDOUBLING=$(poetry run python3 src/main.py -t instances/tsplib/ftv33.atsp --multibeta)
if [ "$EXPECTED_TREEDOUBLING" = "$ACTUAL_TREEDOUBLING" ]; then
    echo "passed."
else
    echo "failed."
    echo "Expected output:"
    echo "$EXPECTED_TREEDOUBLING"
    echo
    echo "Actual output:"
    echo "$ACTUAL_TREEDOUBLING"
    echo
    FAILED=true
fi

echo -n "Testing generalized Christofides algorithm... "
ACTUAL_CHRISTOFIDES=$(poetry run python3 src/main.py -c instances/tsplib/ftv33.atsp --multibeta)
if [ "$EXPECTED_CHRISTOFIDES" = "$ACTUAL_CHRISTOFIDES" ]; then
    echo "passed."
else
    echo "failed."
    echo "Expected output:"
    echo "$EXPECTED_CHRISTOFIDES"
    echo
    echo "Actual output:"
    echo "$ACTUAL_CHRISTOFIDES"
    echo
    FAILED=true
fi

if [ "$FAILED" = true ]; then
    exit 1
fi
