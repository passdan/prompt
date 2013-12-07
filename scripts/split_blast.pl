#!/usr/bin/perl
use strict;
use warnings;

unless($@)
{

print "Converting BLASTn result into sample specific files\n";

my $BLASTn_file = $ARGV[0];
my $out_dir = $ARGV[1];

system "mkdir $out_dir/blast/";
open (IN1, '<', $BLASTn_file) or die ("Can't open $BLASTn_file for reading.\n");
open (IDS, '>', "$out_dir/sample_list.txt") or die ("cant open sample_list.txt\n");


my @IDS;
my $data_pos = tell IN1;
while ( my $line = <IN1> ) {
        if ( $line !~ /^#/ ) {
                chomp $line;
                my @fields = split(/\t/, $line);

                my $query = $fields[0];
                        my @q = split(/\|/, $query);
                        push (@IDS, $q[1]);  #FIX THE UNIQ CMD
        }
}

#Filter for uniques
my %seen = ();
my @uniques = ();
foreach my $a (@IDS){
	unless ($seen{$a}){
		push @uniques, $a;
		$seen{$a} = 1;
	}
}

my @handles;
foreach my $id (@uniques){
        open $handles[$id], '>', "$out_dir/blast/$id.blast" or die "Cant open filehandle $id\n";
        print "Split $id.blast\n";
}
seek IN1, $data_pos, 0;
while (my $in1 = <IN1>){
        if ($in1 =~ /.+\|(\w+)\s.*/){		
                select $handles[$1];
                print $in1;
        }
		
}

select IDS;
foreach (@uniques){
	print "$_\n";
}
}
