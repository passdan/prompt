#!/usr/bin/perl

##########################################################
##Dan Pass | 03/01/12              			##
##daniel.antony.pass@googlemail.com			##
##for use in generating html talbes from PROMpT output  ##
##########################################################

use strict;
use warnings;

##usage  ./gen_taxa_html tmp_dir site level
##MUST HAVE 'html_template' IN THE SCRIPTS DIRECTORY!

my $site = $ARGV[0];
my $level = $ARGV[1];

my $file = "DTM" . $site . "_" . $level . ".txt";

open TAXA, "$site/$file" or die "Cannot open $file abundance file\n";
open TEMPLATE, "../../scripts/html_template" or die "!!Template file is not present in script directory!!\n";

$file =~ s/.*_(.+).txt/$1/;
open OUTFILE, '>', "html_files/DTM$site/$file.html" or die "Couldn't open $file.html for writing\n";

my %unsorted = ();
my $size;
my $cumulative = 0;

while (my $line = <TAXA>){
       	chomp $line;
        my @cols = split(/\t/, $line);
	$unsorted{$cols[0]} = sprintf("%.3f", $cols[1]);
	$size++;	
}
close TAXA;

my @keys = sort { $unsorted{$b} <=> $unsorted{$a} } keys(%unsorted);
my @vals = @unsorted{@keys};


select OUTFILE;
while (<TEMPLATE>){
	if (/XXTAXALEVELXX/){
		s/XXTAXALEVELXX/$file/;
		print;
	}elsif(/XXTITLEXX/){
	        s/XXTITLEXX/Microscopy:DTM$site:$file/;
        	print;
	}elsif (/(^var chartData)/){
		print "$1 =\[";
		my $count = 0;
		my $last = $size -1;
		foreach my $in (@keys){
			#print "$in,\n";
			if ($in eq $keys[-1] ) {
				print "\{$file:\"$in\",abundance:$vals[$count]\}\]\n";
				last;
			}else{
				print "\{$file:\"$in\",abundance:$vals[$count]\},\n";
			}
			$count++;
		}
	}else{ 
		print;
	}
}
close OUTFILE;

