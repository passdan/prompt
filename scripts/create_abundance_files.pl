#!/usr/bin/perl
use strict;
use warnings;

#Create abundance files from blastn output

my $usage = "\nusage :\n\n$0 <BLASTn_file> <total_read_number> <processing directory> <cluster size file> \n\n";

my $BLASTn_file = $ARGV[0] ;
my $total_read_number = $ARGV[1];
my $tmp_dir = $ARGV[2];
my $clust_abun = $ARGV[3];

print "Calculating abundances for $BLASTn_file\n";

open BLAST, "< $tmp_dir/" . "blast_files/" . "$BLASTn_file" or die("\nPath: $tmp_dir/" . "blast_files/" . "$BLASTn_file\n$!");
print "Processing: blast in = $tmp_dir/" . "blast_files/" . "$BLASTn_file\n";

open TAXA, "< taxonomy/all_taxa.txt" or die "Can't open all_taxa.txt for reading.\n";
open NAMES, " < taxonomy/names.dmp" or die "Can't open names.dmp file\n";
open ABUN, "< $tmp_dir/clusters.txt" or die "Can't open cluster.txt abundance file\n";

my $sample = $BLASTn_file;
$sample =~ s/\..*//;

my %Match = ();

my %Evalue = ();

while ( my $line = <BLAST> ) 
{

	if ( $line !~ /^#/ ) {
		chomp $line;

		my @fields = split(/\t/, $line);

		my $query = $fields[0];

		my $match = $fields[1];

		my $evalue = $fields[10];

		if ((not exists  $Match{$query}) or ($evalue <  $Evalue{$query})){	# only take the best hit
			$Match{$query} = $match;
			$Evalue{$query} = $evalue;
		}
	}
}
close BLAST;

my $line = <TAXA>;

my %hash_species ;
my %hash_genus ;
my %hash_family;
my %hash_order;
my %hash_class;
my %hash_phylum;

while(my $line = <TAXA>)
{
	chomp $line;
	
	my @fields = split(/\t/, $line);
	
	$hash_species{$fields[0]} = $fields[1];			##Numbers changed to represent eukaryota
	$hash_genus{$fields[0]} = $fields[2] ;			##and to accomodate tables produced from
	$hash_family{$fields[0]} = $fields[3] ;			##http://www.ncbi.nlm.nih.gov/Taxonomy/T
	$hash_order{$fields[0]} =$fields[4] ;			##axIdentifier/tax_identifier.cgi
	$hash_class{$fields[0]} = $fields[6] ;			##DAN
	$hash_phylum{$fields[0]} = $fields[8] ;			
	
}
close TAXA;

my %abun;
my $total_abundance = 0;

while(my $pair = <ABUN>){
	chomp $pair;
	my @ab = split(/\t/, $pair);

	$abun{$ab[0]} = $ab[1];
}
close ABUN;

my %names;

while(my $line =<NAMES>){

	chomp $line;
	my @fields = split/\t/, $line;
	
	if ( $fields[6] eq 'scientific name' ){

		if (exists $names{$fields[0]}){
			print "Duplicate keys in the hash\n";
		}else{
			$names{$fields[0]} = $fields[2];
		}
	}
}
close NAMES;

my $tax_level;
my %hash;

for (my $i=1; $i<=6; $i++){

	if( $i == 1 ){
		$tax_level = 'species';
		%hash = %hash_species;
	}elsif( $i == 2 ){
		$tax_level = 'genus';
		%hash = %hash_genus;
	}elsif( $i == 3 ){
		$tax_level = 'family';
		%hash = %hash_family;
	}elsif( $i == 4 ){
		$tax_level = 'order';
		%hash = %hash_order;
	}elsif( $i == 5 ){
		$tax_level = 'class';
		%hash = %hash_class;
	}elsif( $i == 6 ){
		$tax_level = 'phylum';
		%hash = %hash_phylum;
	}
	
	open OUT, '>',"$tmp_dir/abundance_files/$sample/$sample".'_'."$tax_level"."_proportion" or die "Can't open file $tmp_dir/abundance_files/$sample/$sample".'_'."$tax_level"."_proportion: $!";
	
	my %Count;

	#my $total_abundance = 0 ;
	
	while (my ($key, $value) = each (%Match)) {
		#print "Key: $key Value: $value\n";
#		print "hash{key} = hash{$key} = $hash{$key}\n";
#		print "hash{value} = hash{$value} = $hash{$value}\n";
		#print "hash{$value} = $hash{$value}\n";
		#next;
		my $tax_id = $hash{$value};
		print "$tax_id : $key : $abun{$key}\n";
#		next;
		if (exists $Count{$tax_id}){
			$Count{$tax_id} = $Count{$tax_id} + $abun{$key};
		}else{
			$Count{$hash{$value}} = $abun{$key} ;
		}
		#
		#if ($hash{$value} ne 'NULL'){
		#	$total_abundance ++ ;
		#}
	}

	while (my ($key, $value) = each (%Count)) {
		#print "Key: $key Value $value\n";
			
		if ($key ne 'NULL'){
			my $prop = $value / $total_read_number;
			my $round = sprintf "%.3f", $prop;
			print OUT $key,"\t", $names{$key} ,"\t", $prop, "\n";
		}
	}
		print OUT "Assigned read proportion : ", $total_abundance / $total_read_number , "\n";
		print OUT "Total read number : ", $total_read_number , "\n";
close OUT;
}
