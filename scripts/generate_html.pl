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

my $tmp_dir = $ARGV[0];
my $script_dir = $ARGV[1];
my $site = $ARGV[2];
my $level = $ARGV[3];

my $file = $site . "_" . $level . "_proportion";

open TAXA, "$tmp_dir/abundance_files/$site/$file" or die "Cannot open $file abundance file\n";
open TEMPLATE, "$script_dir/piechart_template.html" or die "!!Template file is not present in script directory!!\n";

$file =~ s/.*_(.+)_proportion/$1/;
open OUTFILE, '>', "$tmp_dir/html_files/$site/$file.html" or die "Couldn't open $tmp_dir/html_files/DTM$site/$file.html for writing\n";

my @fields;
my $size;
my $cumulative = 0;

while (my $line = <TAXA>){
        	chomp $line;
        if ($line =~ /^Proportion/){
        	        last;
        }else{
        	my @cols = split(/\t/, $line);
#	if ($cols[1] > 0.5){
		my $round = sprintf("%.3f", "$cols[1]");
	        push @fields, "\{\"$file\":\"$cols[0]\",\"abundance\":$round\}";
#	}else{
#		$cumulative = $cumulative + $cols[1];
	}
	$size++;	
#	}
}
close TAXA;

my @sorted = 	map {$_->[0]}
		sort { $b->[2] cmp $a->[2] ||
		       $a->[1] cmp $b->[1] }
		map {chomp;[$_,split(/,/)]} @fields;

#my $cum_round = sprintf("%.3f", $cumulative);
#push (@sorted, "\{\"$file\":\"other\",\"abundance\":$cum_round\}");

select OUTFILE;
while (<TEMPLATE>){
	if (/XXTAXALEVELXX/){
		s/XXTAXALEVELXX/$file/;
		print;
       }elsif(/XXTITLEXX/){
                s/XXTITLEXX/NGS | $site | $file/;
                print;
       }elsif(/XXURLXX/){
                s/XXURLXX/$site/g;
                print;
	}elsif (/(XXINPUTDATAXX)/){
		#print "$1 =\[";
		my $count = 0;
		my $last = $size -1;
		foreach my $in (@sorted){
			#print "$in,\n";
			if ($in eq $sorted[-1] ) {
				print "$in\n";
				#print "$in\]\n";
				last;
			}else{
				print "$in,\n";
			}
			$count++;
		}
	}else{ 
		print;
		}
}
close OUTFILE;

