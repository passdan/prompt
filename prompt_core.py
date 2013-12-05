#!/usr/bin/python
#prompt-core-processes
#daniel.antony.pass@googlemail.com


import sys
import getopt
args = '-i'.split()

import re
from subprocess import call
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline

in_fasta = 0
seq_no = 0
lengths = []
in_fasta = "18s.fas"
database = "blast_db/randomised_diatom.fasta"
indir = "test_data/"
tmpdir = "tmp_dir/"


try:
    open_fasta = open(indir + in_fasta, "rU")
except IOError:
    print "Cannot find input fasta"


def main():
    #process infiles
    print "Processing infiles"

    for record in SeqIO.parse(open_fasta, "fasta"):
        lengths.append(len(record.seq))
    
    global seq_no
    seq_no = len(lengths)

    print "Average length of", seq_no, "input sequences is ", sum(lengths)/seq_no, "base pairs"

    #cd-hit
    #print "Passing to CD-HIT for data reduction"
    cdhit(in_fasta)

    #do blast
    #blastn(in_fasta, database)
        ##can this take the cdhit output?

    #create outfiles
    ##Merge blast and cdhit


    #build web files


def blastn(fas, db):
    print("blasting " + str(seq_no) + " sequences against the " + db + " database")

    blast_in = (indir + fas)
    blast_out = (tmpdir + fas + ".blastn")


    blastn_cline = NcbiblastnCommandline(query=blast_in, db=db, evalue=0.001, outfmt=6, out=blast_out, num_threads=4)

    stdout, stderr = blastn_cline()

    blast_err_log = open(tmpdir + "blast_err.txt", "w")
    blast_stdout_log = open(tmpdir + "blast_stdout.txt", "w")

    blast_err_log.write(stderr)
    blast_stdout_log.write(stdout)


def cdhit(fas):
    cdhit_in = (indir + fas)
    global cdhit_out
    cdhit_out = (tmpdir + fas + "_cdhitout.fa")
    cd_stdout = (tmpdir + "cdhit_stdout.txt")
    cd_stderr = (tmpdir + "cdhit_sterr.txt")


    call(["cd-hit-454","-i",cdhit_in,"-o",cdhit_out])

if __name__ == "__main__":
    main()
