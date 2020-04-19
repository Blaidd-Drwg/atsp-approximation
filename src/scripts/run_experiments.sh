#!/bin/bash

PARENTDIR=$(dirname "$0")/../..
python3 "$PARENTDIR/src/main.py" >/dev/null 2>&1 || (echo "Error when executing main.py without arguments. Did you run 'poetry shell'?" && exit 1)

OUTPUTDIR="$PARENTDIR/output"
echo Outputting results to \'$(realpath --relative-to="." "$OUTPUTDIR")\'
mkdir -p "$OUTPUTDIR"
for instance in $PARENTDIR/instances/tsplib/*.atsp; do
    INSTANCE_NAME=$(basename "$instance")
    echo -n "$INSTANCE_NAME: "
    echo -n "Running tree-doubling... "
    python3 "$PARENTDIR/src/main.py" -t --multibeta "$instance" > "$OUTPUTDIR/$INSTANCE_NAME.t"
    echo -n "Running Christofides... "
    python3 "$PARENTDIR/src/main.py" -c --multibeta "$instance" > "$OUTPUTDIR/$INSTANCE_NAME.c"
    echo done
done
