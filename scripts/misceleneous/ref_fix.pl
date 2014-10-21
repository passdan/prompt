#!/usr/bin/perl

$file = $ARGV[0];

open OUT, ">", "DTM$file";
select OUT;

while(<>){
	chomp(@cols = split('\t', $_));
	if ($cols[0] == "0"){
		next;
	}else{
		if ($cols[1] eq "Row Labels"){
			next;
		}else{
			print "$cols[1]\t$cols[0]\n";
		}
	}
}
exec "rm $file";
