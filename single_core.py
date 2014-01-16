#!/usr/bin/python
#prompt-core-processes
#daniel.antony.pass@googlemail.com

#######################
##This script runs the backbone of prompt. External packages 
##are called from here but additional scripts which are refered
##to can be found in the ./scripts folder.
##
##Functions are listed alphabetically.
#######################


import sys
import getopt
args = '-i'.split()

import re
from subprocess import call
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline

seq_no = 0
lengths = []
in_fasta = "18s.fas"
bcfile = "barcodes.txt"
database = "blast_db/dia_db"
indir = "test_data/"
tmpdir = "tmp_dir2/"
barcoded = 0

##parameters
blast_minscore = 100


try:
    open_fasta = open(indir + in_fasta, "rU")
except IOError:
    print "Cannot find input fasta"


def main():
    #process infiles
    print "Processing infiles"

    process_infiles(open_fasta,bcfile)

    #cd-hit
    print "Passing to CD-HIT for data reduction"
#    cdhit_fas = cdhit(in_fasta)

    #do blast
    print "Passing to blastn for taxonomic assignment"
#    blast_out = blastn(cdhit_fas, database)

    ##split blast output into sample files
#    call(["perl", "scripts/split_blast.pl", blast_out, tmpdir])

    ##Create abundance files
#    sample_list = open(tmpdir + "sample_list.txt", "rU")
    call(["mkdir", tmpdir + "abundance_files"])

    for sample in sample_list:
        sample_path = "split_blasts/" + sample.rstrip() + ".blast"
        call(["perl", "scripts/create_abundance_files.pl", sample_path, "529", tmpdir])
        #call(["perl", "scripts/create_abundance_file.pl", sample, seq_no, tmpdir])

    #create outfiles
    ##Merge blast and cdhit


    #build web files


def blastn(fas, db):
    #print("blasting " + str(seq_no) + " sequences against the " + db + " database")  ##fix
    print("blasting cdhit sequences against the " + db + " database")

    blast_in = (fas)
    blast_out = (fas + ".blastn")


    blastn_cline = NcbiblastnCommandline(query=blast_in, db=db, evalue=0.001, outfmt=6, out=blast_out, num_threads=4)

    stdout, stderr = blastn_cline()

    blast_err_log = open(tmpdir + "blast_err.txt", "w")
    blast_stdout_log = open(tmpdir + "blast_stdout.txt", "w")

    blast_err_log.write(stderr)
    blast_stdout_log.write(stdout)

    #filter blast
    #call(["perl", "scripts/filter_blast.pl", blast_out, blast_minscore])

    return blast_out


def cdhit(fas):
    cdhit_in = (indir + fas)
    global cdhit_out
    cdhit_out = (tmpdir + fas + "_cdhitout.fa")
    cd_stdout = (tmpdir + "cdhit_stdout.txt")
    cd_stderr = (tmpdir + "cdhit_sterr.txt")

    call(["cd-hit-454","-i",cdhit_in,"-o",cdhit_out])

    return cdhit_out

def process_infiles(open_fasta,barcodes):

    for record in SeqIO.parse(open_fasta, "fasta"):
        lengths.append(len(record.seq))
    
    global seq_no
    seq_no = len(lengths)

    print "Average length of", seq_no, "input sequences is ", sum(lengths)/seq_no, "base pairs"

if __name__ == "__main__":
    main()
