import argparse
from glob import glob
from os import path

parser = argparse.ArgumentParser()
parser.add_argument("outfile")
parser.add_argument("directory")
args = parser.parse_args()

target = args.outfile
directory = args.directory

files = glob(f"{directory}/*.atsp.?")

stuff = []
for f in files:
    with open(f) as handle:
        lines = [l.strip() for l in handle]
    if len(stuff)==0:
        stuff.append(lines[0] + ", graph, algo")
    for line in lines[1:]:
        basename = path.basename(f)
        graph = basename.split(".atsp")[0]
        if basename.endswith("c"):
            algo = "christofides"
        else:
            algo = "tree-doubling"
        line += f", {graph}, {algo}"
        stuff.append(line)

with open(target, "w") as handle:
    towrite = [l+"\n" for l in stuff]
    handle.writelines(towrite)




