#!/usr/bin/python
#prompt-core-processes
#daniel.antony.pass@googlemail.com

import getopt
args = '-i'.split()

from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline


in_fasta = "18s_small.fas"
hand = in_fasta = s/(.*).fasta/\1/

def main():
    #process infiles

    #cd-hit

    #do blast
    blastn(in_fasta)

    #create outfiles

    #build web files


def blastn(fas):
    #do blastn
    blastn_cline = NcbiblastnCommandline(query=fas, db="~/projects/MetaMOD/blastdb/dia_db", evalue=0.001, outfmt=6, out=".blastn")

    
    blastn_cline()

    #stdout, stderr = blastn_cline()

#for seq_record in SeqIO.parse("18s.fas", "fasta"):
#    blastn(seq_record.fasta)

if __name__ == "__main__":
    main()
