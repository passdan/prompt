#!/usr/bin/python


import sys
import getopt
from subprocess import call

indir = "test_data/"
sample_list = "sample_list.txt"

open_sample_list = open(indir + sample_list, "rU")



for sample in open_sample_list:
    rows = sample.split('\t') 
    sampleID =  rows[0]

    print "Running prompt_core on sample: " + sampleID
    call(["./prompt_core.py", sampleID])
