#!/usr/bin/perl
use warnings;

open OUTFILE, ">out1.txt";
select OUTFILE;
print "Hello World!\n";
