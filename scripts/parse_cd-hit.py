#!/usr/bin/python

import sys
import re


in_file = sys.argv[1]
tmp_dir = sys.argv[2]

lines = open(in_file, "rU")
clust = open(in_file + ".parse", "w")

C = "OTU"
a = "size"

def write_out(size, name):
    clust.write( name + "\t" +  str(size) + "\n")


for line in lines:
    h = re.search(r">Cluster", line)
    m = re.search(r"(\w+)\.{3}\s\*", line)

    if h:      
        write_out(a,C)
        a = 0
    else:
        a += 1

    if m:
        C = m.group(1) 

write_out(a,C)

