#!/usr/bin/python
#prompt-core-processes
#daniel.antony.pass@googlemail.com

from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline

for seq_record in SeqIO.parse("test.fasta", "fasta"):
    print seq_record.id
    

def main():
    #process infiles

    #cd-hit

    #blastn

    #create outfiles

    #build web files


def blastn(in_fasta):
	#do blastn
	blastn_cline = NcbiblastnCommandline(query=in_fasta, db="nr", evalue=0.001, outfmt=8, out="opuntia.blastn")    


