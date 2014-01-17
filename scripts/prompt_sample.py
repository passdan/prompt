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

indir = sys.argv[1]
sample = sys.argv[2]

in_fasta = sample + ".fas"
database = "blast_db/dia_db"
seq_no = 0
lengths = []
tmpdir = "tmp_dir/"
taxa_list = ("species","genus","family","order","class","phylum")

##parameters
blast_minscore = 100


try:
    open_fasta = open(indir + in_fasta, "rU")
except IOError:
    print "Cannot find input:" + indir + in_fasta


def main():
    #process infiles
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Processing infiles"

#    process_infiles(open_fasta)

    #cd-hit
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Passing to CD-HIT for data reduction"
#    cdhit_fas = cdhit(in_fasta)

    #do blast
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Passing to blast for taxonomic assignment"
#    blast_out = blastn(cdhit_fas, database)

    ##split blast output into sample files
#    call(["perl", "scripts/split_blast.pl", blast_out, tmpdir])

    ##Create abundance files
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Converting blast output into abundance files"
#    call(["mkdir", tmpdir + "abundance_files/" + sample])
#    call(["perl", "scripts/create_abundance_files.pl", str(sample) + ".blast", str(seq_no), tmpdir])

    #build web files
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "converting output files into html webfiles"
    call(["mkdir", tmpdir + "html_files/" + sample])
    for level in taxa_list:
        print "Generating html file:" + sample + "-" + level
        call(["perl", "scripts/gen_taxa_html.pl", tmpdir, sample, level])

def blastn(fas, db):
    #print("blasting " + str(seq_no) + " sequences against the " + db + " database")  ##fix
    print("blasting cdhit sequences against the " + db + " database")

    blast_in = (fas)
    blast_out = (tmpdir + "blast_files/" + sample + ".blast")


    blastn_cline = NcbiblastnCommandline(query=blast_in, db=db, evalue=0.001, outfmt=6, out=blast_out, num_threads=3)

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

    call(["scripts/parse_cd-hit.py", cdhit_out + ".clstr", tmpdir])

    return cdhit_out

def process_infiles(open_fasta):

    call(["mkdir", tmpdir + "abundance_files/" + sample])

    for record in SeqIO.parse(open_fasta, "fasta"):
        lengths.append(len(record.seq))
    
    global seq_no
    seq_no = len(lengths)

    print "Average length of", seq_no, "input sequences is ", sum(lengths)/seq_no, "base pairs"

if __name__ == "__main__":
    main()
