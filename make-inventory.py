import glob
import os
import sys
import re
import urllib
import requests
import time
from itertools import groupby


CARD_NAMES_API = r"https://api.scryfall.com/cards/named?"


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
rich_manifest = []
for name, st, count in sorted(manifest, key=lambda x: (x[1], x[0])):
    uri = CARD_NAMES_API + urllib.parse.urlencode({'fuzzy': name, 'set': st}) 
    sys.stderr.write(f"Requeting: {uri}\n")
    r = requests.get(uri)
    color_identity = ''.join(r.json()['color_identity'])
    img_uri = r.json()['image_uris']['small']
    cmc = int(r.json()['cmc'])
    rich_manifest.append((str(count), name, st, color_identity, str(cmc), img_uri))
    time.sleep(0.1)

for m in sorted(rich_manifest, key=lambda x: (x[2], x[3], x[1])):
    sys.stdout.write(' '.join(m) + '\n')