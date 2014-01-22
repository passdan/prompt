#!/usr/bin/python

import sys

in_file = sys.argv[1]
pc_match = sys.argv[2]

lines = open(in_file, "rU")
out_file = open(in_file + "_filter", "w")

for line in lines:
    cols = (line.split('\t'))

    if (float(cols[2]) < float(pc_match)):
        cols[1] = "No_Match"

    out_file.write('\t'.join(cols))
