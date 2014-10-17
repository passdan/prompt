#!/usr/bin/python


import sys
import ConfigParser
from subprocess import call

Config = ConfigParser.ConfigParser()


sample_dir = "input_fasta/"
sample_list = "sample_list.txt"
tmp_dir = "tmp_dir/"
blast_db = "blast_db/composite"
blast_homology = "96"
core_no = "14"

#log_file = open(tmp_dir + Run_Log.txt, 'w')

#log_file.write("##Parameters used in this analysis run##")

call(["rm", "-r", "tmp_dir"])
call(["mkdir", tmp_dir])
call(["mkdir", tmp_dir + "/abundance_files"])
call(["mkdir", tmp_dir + "/cdhit_files"])
call(["mkdir", tmp_dir + "/blast_files"])
call(["mkdir", tmp_dir + "/html_files"])


open_sample_list = open(sample_dir + sample_list, "rU")


for sample in open_sample_list:
    rows = sample.split('\t') 
    sampleID =  rows[0]

    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Running prompt_sample.py on sample " + sampleID + " (" + rows[1].rstrip() + ")"
    call(["scripts/prompt_sample.py", sample_dir, sampleID, tmp_dir, blast_db, blast_homology, core_no])
