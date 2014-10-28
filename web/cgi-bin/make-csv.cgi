#!/usr/bin/perl

use CGI qw(:cgi-lib :standard);  
use Data::Dumper; $Data::Dumper::Useqq=1; 

&ReadParse(%in);                 # This grabs the data passed by the form and puts it in an array

$selection = $in{"selection"};    # Get the samples selected
$taxa = $in{"taxa"};     	  # Get the taxa level

                                 # Start printing HTML document
print<<EOSTUFF; 
Content-type: text/html

<HTML>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>Results</title>
        <link href='https://fonts.googleapis.com/css?family=Chivo:900' rel='stylesheet' type='text/css'>
        <link rel="stylesheet" type="text/css" href="/prompt/stylesheets/stylesheet.css" media="screen">
        <link rel="stylesheet" type="text/css" href="/prompt/stylesheets/pygment_trac.css" media="screen">
        <link rel="stylesheet" type="text/css" href="/prompt/stylesheets/print.css" media="print">
    </head>
    <body>
      <div id="container">
	<div class="inner">

        <header>
	  <center>
          <img src="/prompt/images/prompt-beta.png" alt="PROMpT logo">
          <h2>Navigation</h2>
	  <h4><a href="/prompt/index.html">Home</a> | <a href="/prompt/processing.html">Processing</a> | <a href="/prompt/results.php">Results</a></h4>
        </header>
        <hr>
EOSTUFF

@samples = split("\0", $selection);

system `rm /var/www/prompt/tmp/tmplatest.txt`;
system `touch /var/www/prompt/tmp/tmplatest.txt`;

print "<h1>Analysing:</h1>";
$samplestring = $taxa;

foreach $i (@samples){
	chomp;
	$samplestring .=",$i";
	print "$i<br>\n";
	@g = split(/_/, $i);
	$file = "/var/www/prompt/analyses/abun/$g[0]/$g[1]/$g[1]_$taxa" . "_proportion";
	push (@paths, $file);
}


foreach $path (@paths){
	chomp;
	$i++;
	$sedsort = "sed 's/ (.*)//' < $path | sort -k1 | grep -v 'Proportion' >/var/www/prompt/tmp/tmpsort.txt";
	system("$sedsort");
	if ($i == 1){
		system("mv /var/www/prompt/tmp/tmpsort.txt /var/www/prompt/tmp/tmplatest.txt");
	}
	if ($i > 1){
		$join = "join -e 0 -o auto -a1 -a2 /var/www/prompt/tmp/tmplatest.txt /var/www/prompt/tmp/tmpsort.txt > /var/www/prompt/tmp/tmpjoin.txt";
		system("$join");
		system("mv /var/www/prompt/tmp/tmpjoin.txt /var/www/prompt/tmp/tmplatest.txt");
	}
}

system("echo $samplestring >/var/www/prompt/tmp/current_selection.csv");
system("sed 's/ /,/g' < /var/www/prompt/tmp/tmplatest.txt >> /var/www/prompt/tmp/current_selection.csv"); 

system('R --vanilla --slave < /usr/lib/cgi-bin/heatmap.r');
system('R --vanilla --slave < /usr/lib/cgi-bin/nmds.r');

print<<EOF;      
  <h2>Download data: <a href="/prompt/tmp/current_selection.csv">Current_selection.csv</a></h2>
  <hr>
  <center>
  <h2><a href="/prompt/tmp/heatmap.png">Heatmap</a></h2>
   <a href="/prompt/tmp/heatmap.png"><img src="/prompt/tmp/heatmap.png" alt="heatmap" width=600 height=auto>
  <h2><a href="/prompt/tmp/nmds.png">NMDS</a></h2>
   <a href="/prompt/tmp/nmds.png"><img src="/prompt/tmp/nmds.png" alt="nmds" width=600 height=auto>
  </center>
</BODY>
</HTML>
EOF
