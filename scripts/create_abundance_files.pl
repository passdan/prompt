#!/usr/bin/perl
use strict;
use warnings;

#Create abundance files from blastn output

my $usage = "\nusage :\n\n$0 <BLASTn_file> <total_read_number> <output directory> \n\n";

my $BLASTn_file = $ARGV[0] ;
my $total_read_number = $ARGV[1];
my $output_dir = $ARGV[2];


print "Calculating abundances for $BLASTn_file\n";

open IN1, "< $output_dir/blast/$BLASTn_file.blast" or die("Can't open $BLASTn_file for reading.\n");
print "blast in = $output_dir/blast/$BLASTn_file.blast";

open IN2, "< /taxonomy/all_taxa.txt" or die "Can't open all_taxa.txt for reading.\n";
open IN3, " < /taxonomy/names.dmp";

my $sample = $BLASTn_file;
$sample =~ s/\..*//;
system "mkdir $output_dir/abundance/$sample/";

my %Match = ();

my %Evalue = ();

while ( my $line = <IN1> ) 
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
close IN1;

my $line = <IN2>;

my %hash_species ;
my %hash_genus ;
my %hash_family;
my %hash_order;
my %hash_class;
my %hash_phylum;
my %hash_superkingdom;

while(my $line = <IN2>)
{
	chomp $line;
	
	my @fields = split(/\t/, $line);
	
	$hash_species{$fields[0]} = $fields[1];			##Numbers changed to represent eukaryota
	$hash_genus{$fields[0]} = $fields[2] ;			##and to accomodate tables produced from
	$hash_family{$fields[0]} = $fields[3] ;			##http://www.ncbi.nlm.nih.gov/Taxonomy/T
	$hash_order{$fields[0]} =$fields[4] ;			##axIdentifier/tax_identifier.cgi
	$hash_class{$fields[0]} = $fields[6] ;			##DAN
	$hash_phylum{$fields[0]} = $fields[8] ;			
	$hash_superkingdom{$fields[0]} = $fields[9] ;
	
}
close IN2;

my %names ;
#my %taxid ;

while(my $line =<IN3>){

	chomp $line;
	my @fields = split/\t/, $line;
	
	if ( $fields[6] eq 'scientific name' ){

		if (exists $names{$fields[0]}){
			print "Exists the same key of the name hash table !! \n";
		}else{
			$names{$fields[0]} = $fields[2];
			#$taxid{$fields[2]} = $fields[0];
		}
	}
}
close IN3;

my $tax_level ;
my %hash ;

for (my $i=1 ; $i<=7 ; $i++){

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
	}elsif( $i == 7 ){
		$tax_level = 'superkingdom';
		%hash = %hash_superkingdom;
	}
	
	open OUT, '>',"$output_dir/abundance/$sample/$BLASTn_file".'_'."$tax_level"."_proportion" or die("Can't open $sample/$BLASTn_file".'_'."$tax_level"."_proportion for writing.\n");
	
	my %Count;

	my $total_abundance = 0 ;
	
	while (my ($key, $value) = each (%Match)) {
		if (exists $Count{$hash{$value}}){
			$Count{$hash{$value}}++;
		}else{
			$Count{$hash{$value}} = 1 ;
		}
	
		if ($hash{$value} ne 'NULL'){
			$total_abundance ++ ;
		}
	}

	while (my ($key, $value) = each (%Count)) {
			
		if ($key ne 'NULL'){
			my $prop = $value / $total_abundance;
			my $round = sprintf "%.3f", $prop;
			print OUT $key,"\t", $names{$key} ,"\t", $prop, "\n";
		}
	}
		print OUT "Assigned read proportion : ", $total_abundance / $total_read_number , "\n";
		print OUT "Total read number : ", $total_read_number , "\n";
close OUT;
}
