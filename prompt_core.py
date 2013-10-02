#!/usr/bin/python
#prompt-core-processes
#daniel.antony.pass@googlemail.com

import sys
import getopt
args = '-i'.split()

from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline

in_fasta = 0
seq_no = 0
lengths = []

try:
    in_fasta = open("test_data/18s.fas", "rU")
except IOError:
    print "Cannot find in_fasta"


def main():
    #process infiles
    print "Processing infiles"

    for record in SeqIO.parse(in_fasta, "fasta"):
        lengths.append(len(record.seq))
    
    global seq_no
    seq_no = len(lengths)

    print "Average length of", seq_no, "input sequences is ", sum(lengths)/seq_no, "base pairs"
    #cd-hit
    print "Passing to CD-HIT for data reduction"

    #do blast
    #blastn(in_fasta)

    #create outfiles

    #build web files


def blastn(fas):
    #do blastn
    pass

    #blastn_cline = NcbiblastnCommandline(query=fas, db="~/projects/MetaMOD/blastdb/dia_db", evalue=0.001, outfmt=6, out=".blastn")

    #blastn_cline()

    #stdout, stderr = blastn_cline()

#for seq_record in SeqIO.parse("18s.fas", "fasta"):
#    blastn(seq_record.fasta)

if __name__ == "__main__":
    main()
