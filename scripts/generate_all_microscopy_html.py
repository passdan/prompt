#!/usr/bin/python

import sys
from subprocess import call 

files = sys.argv[1]

samples = open(files, "rU")

taxa_list = ("species","genus","family","class")

for sample in samples:
    call(["mkdir", "html_files/DTM" + sample.rstrip()])
    for level in taxa_list:
        print "Generating html file:" + sample + "-" + level
        call(["perl", "../../scripts/gen_microscopy_html.pl", sample.rstrip(), level])
