#!/bin/bash

cut -f1 ../taxonomy/taxa_dictionary.txt > tmp.txt
fasta_pull global.fas tmp.txt
mv pulled_seqs.fasta composite.fas
makeblastdb -in composite.fas -out composite -dbtype nucl

