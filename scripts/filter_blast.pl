#!/usr/bin/perl -w

# Filter the BLAST hits with bit score less than min-score

use strict;

my $usage = "\nusage :\n\n$0 <BLAST_file> <min-score> <output directory>\n\n";

die $usage unless ($#ARGV == 2);

my ($BLAST_file, $min_score ,$output_dir ) = @ARGV;

my $file = "$BLAST_file".'_tmp' ;

open IN, "< $BLAST_file" or die("Can't open $BLAST_file for reading.\n");
open OUT, "> $output_dir/$file" or die("Can't open $file for reading.\n");

while ( my $line = <IN> ) 
{
	chomp $line;

	my @fields = split(/\t/, $line);

	if ($fields[11] > $min_score ){
	
		print OUT "$line\n";
	}
}
close IN;
close OUT;

system "mv $file $BLAST_file";

system "rm -f $file";

