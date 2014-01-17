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
my $site = $ARGV[1];
my $level = $ARGV[2];

my $file = $site . "_" . $level . "_proportion";

#foreach my $file (@files){
	open TAXA, "$tmp_dir/abundance_files/$site/$file" or die "Cannot open $file abundance file\n";
	open TEMPLATE, "./scripts/html_template" or die "!!Template file is not present in script directory!!\n";

	$file =~ s/.*_(.+)_proportion/$1/;
	print $file;
	open OUTFILE, '>', "$tmp_dir/html_files/$site/$file.html" or die "Couldn't open $file.html for writing\n";

	my @fields;
	my $size;
	my $cumulative = 0;

	while (my $line = <TAXA>){
        	chomp $line;
	        if ($line =~ /^Ass/){
        	        last;
	        }else{
        	my @cols = split(/\t/, $line);
		if ($cols[2] > 0.005){
			my $round = sprintf("%.3f", "$cols[2]");
		        push @fields, "\{$file:\"$cols[1]\",abundance:$round\}";
		}else{
			$cumulative = $cumulative + $cols[2];
		}
		$size++;	
		}
	}
	close TAXA;

	my @sorted = 	map {$_->[0]}
			sort { $b->[2] cmp $a->[2] ||
			       $a->[1] cmp $b->[1] }
			map {chomp;[$_,split(/,/)]} @fields;

	my $cum_round = sprintf("%.3f", $cumulative);
	push (@sorted, "\{$file:\"other\",abundance:$cum_round\}");

		select OUTFILE;
		while (<TEMPLATE>){
			if (/XXTAXALEVELXX/){
			s/XXTAXALEVELXX/$file/;
			print;
		}elsif (/(^var chartData)/){
			print "$1 =\[";
			my $count = 0;
			my $last = $size -1;
			foreach my $in (@sorted){
				#print "$in,\n";
				if ($count == $last ) {
					print "$in\]\n";
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
#}
