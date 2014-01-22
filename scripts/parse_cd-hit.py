#!/usr/bin/python

import sys
import re


in_file = sys.argv[1]
tmp_dir = sys.argv[2]

lines = open(in_file, "rU")
clust = open(in_file + ".parse", "w")

C = "OTU"
a = "size"

for line in lines:

    m = re.search(r"(\w+)\.{3}\s\*", line)
    if m:
	
        C = m.group(1) 

    h = re.search(r">Cluster", line)
    if h:
        clust.write( C + "\t" +  str(a) + "\n")
        a = 0
    else:
        a += 1
