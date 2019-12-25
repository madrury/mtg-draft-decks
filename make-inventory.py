import glob
import os
import sys
import re
from itertools import groupby

dir = sys.argv[1]

# Build up a list of all the 
cards = []
for path in glob.glob(dir + '/*.txt'):
    fnm = os.path.split(path)[-1]
    name, st = re.match(r'(\w+)-(\w+)\.txt', fnm).groups()
    for n, line in enumerate(open(path, 'r')):
        # Skip the first two lines, which are boilerplate.
        if n < 2:
            continue
        count, name = line.strip().split(' ', maxsplit=1)
        cards.append((name, st, int(count)))

# Deduplicate the list and count how many cards we have.
manifest = []
for (name, st), grp in groupby(sorted(cards, key=lambda x : x[0]), key=lambda x: (x[0], x[1])):
    tally = (name, st, sum(x[2] for x in grp))
    manifest.append(tally)

# Write the manifest to standard output, sorted by set.
for name, st, count in sorted(manifest, key=lambda x: (x[1], x[0])):
    sys.stdout.write(f"{count} {name} {st}\n")
    

