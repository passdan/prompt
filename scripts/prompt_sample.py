#!/usr/bin/python
#prompt-core-processes
#daniel.antony.pass@googlemail.com

#######################
##This script runs the backbone of prompt. External packages 
##are called from here but additional scripts which are refered
##to can be found in the ./scripts folder.
#######################

import sys
import re
from subprocess import call
import subprocess
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline

indir = sys.argv[1]
sample = sys.argv[2]
tmpdir = sys.argv[3]
database = sys.argv[4]
blast_homology = sys.argv[5]
multicore_no = sys.argv[6]
script_dir = sys.argv[7]

in_fasta = sample + ".fas"

seq_no = 0
lengths = []

taxa_list = ("refseq","species","genus","family","class")
divider = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

try:
    open_fasta = open(indir + in_fasta, "rU")
except IOError:
    print "Cannot find input:" + indir + in_fasta


def main():
    #process infiles
    print divider
    print "Processing infiles"

    process_infiles(open_fasta)

    #cd-hit
    print divider 
    print "Passing to CD-HIT for data reduction"
    cdhit_fas = cdhit(in_fasta)

    #do blast
    print divider 
    print "Passing to blast for taxonomic assignment"
    blast_out = blastn(cdhit_fas, database)

    print divider
    print "Filtering Blast results at " + str(blast_homology) + "% required database match"
    print "Filtering " + blast_out
    call([script_dir + "/filter_blast.py", blast_out, str(blast_homology)])

    ##Create abundance files
    print divider
    print "Converting blast output into abundance files"
    call(["mkdir", tmpdir + "abundance_files/" + sample])
    call(["perl", script_dir + "/create_abundance_files.pl", str(sample) + ".blast_filter", str(seq_no), tmpdir, cdhit_clusters])

    #build web files
    print divider
    print "converting output files into html webfiles"
    call(["mkdir", tmpdir + "html_files/" + sample])
    for level in taxa_list:
        print "Generating html file: " + sample + ":" + level
        call(["perl", script_dir + "/generate_html.pl", tmpdir, script_dir, sample, level])

def blastn(fas, db):
    print("blasting cdhit sequences against the " + db + " database")

    blast_in = (fas)
    blast_out = (tmpdir + "blast_files/" + sample + ".blast")


    blastn_cline = NcbiblastnCommandline(query=blast_in, db=db, evalue=0.001, outfmt=6, out=blast_out, num_threads=multicore_no)

    stdout, stderr = blastn_cline()

    blast_err_log = open(tmpdir + "blast_err.txt", "w")
    blast_stdout_log = open(tmpdir + "blast_stdout.txt", "w")

    blast_err_log.write(stderr)
    blast_stdout_log.write(stdout)

    return blast_out


def cdhit(fas):
    cdhit_in = (indir + fas)
    global cdhit_out
    cdhit_out = (tmpdir + "cdhit_files/" + fas + "_cdhitout.fa")
    cd_stdout = (tmpdir + "cdhit_files/ cdhit_stdout.txt")
    cd_stderr = (tmpdir + "cdhit_files/ cdhit_sterr.txt")

    call(["cd-hit-454","-i",cdhit_in,"-o",cdhit_out, "-c", "0.99"])
    #subprocess.Popen(["cd-hit-454","-i",cdhit_in,"-o",cdhit_out], stdout=subprocess.PIPE)

    call([script_dir + "/parse_cd-hit.py", cdhit_out + ".clstr", tmpdir])
    global cdhit_clusters
    cdhit_clusters = (cdhit_out + ".clstr.parse")

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
