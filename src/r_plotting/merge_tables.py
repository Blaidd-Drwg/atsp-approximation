import argparse
from glob import glob
from os import path

parser = argparse.ArgumentParser()
parser.add_argument("outfile")
parser.add_argument("directory")
parser.add_argument("--split", "-s", default='.atsp')
args = parser.parse_args()

target = args.outfile
directory = args.directory
split = args.split

files = glob(f"{directory}/*{split}.?")

stuff = []
for f in files:
    with open(f) as handle:
        lines = [l.strip() for l in handle]
    if len(stuff)==0:
        stuff.append(lines[0] + ",graph,algo")
    for line in lines[1:]:
        if "done" in line:
            continue
        basename = path.basename(f)
        graph = basename.split(split)[0]
        if basename.endswith("c"):
            algo = "christofides"
        else:
            algo = "tree-doubling"
        line += f",{graph},{algo}"
        stuff.append(line)

with open(target, "w") as handle:
    towrite = [l+"\n" for l in stuff]
    handle.writelines(towrite)




