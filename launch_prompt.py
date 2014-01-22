#!/usr/bin/python


import sys
import getopt
from subprocess import call

sample_dir = "input_fasta/"
sample_list = "sample_list.txt"
tmp_dir = "tmp_dir/"
blast_db = "blast_db/HQ"

call(["mkdir", tmp_dir])
call(["mkdir", tmp_dir + "/abundance_files"])
call(["mkdir", tmp_dir + "/blast_files"])
call(["mkdir", tmp_dir + "/html_files"])


open_sample_list = open(sample_dir + sample_list, "rU")


for sample in open_sample_list:
    rows = sample.split('\t') 
    sampleID =  rows[0]

    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Running prompt_sample.py on sample " + sampleID + " (" + rows[1].rstrip() + ")"
    call(["scripts/prompt_sample.py", sample_dir, sampleID, tmp_dir, blast_db])
