<html>
<head>
<title>Results</title>
<style type="text/css">
body {background-image:url('images/diatom_back.jpg');}
</style>
</head>

<body>
<center>
<p><a href="index.html">
<img style="width: 700px; height: 150px;" alt="" src="images/prompt_logo.png"  float:left=""></a>;
<big style="font-family: Calibri;"><font size=7><br>
<hr>
<span style="font-family: Arial Black;"><font size=3>

<h1><center>Data Portal</center></h1>
<h2>Sample Pie charts</h2>

<form name='form1' action='./results.php'>
	<b>Data Origin:</b><br>
	<input type="radio" name="origin" value="SEQ" onclick=submit() selected >Barcode Sequencing
	<input type="radio" name="origin" value="MIC" onclick=submit() >Microscopy
</form>

<form name='form2' action='./results.php'>
	<b>Select a Site:</b><br>
	<input type="hidden" name="origin" value="<?php if(isset($_GET['origin'])) echo $_GET['origin']; ?>" />
<?php
	$origin = $_GET['origin'];
	
	$sites = glob("analyses/pie/$origin/*");
	
	$col1 = 0;

	foreach ($sites as $site){
		$site = preg_replace("/analyses\/pie\/$origin\//i", '', $site);
		print "<input name=\"site\" type=\"radio\" value=\"$site\"  onclick=\"submit()\">$site\n";
		$col1++;
		if ($col1 == 10){
			print "<br>\n";
		}
	
	}
?>
</form>

<?php	
	foreach($_GET as $key=>$value){
		$$key = $value;
		$site_code = $value;
	}
		print "<b>site: $site_code</b>";
	


	$arr = array('class', 'family', 'genus', 'species', 'refseq');
	print "<br><select id='setit' name='url'>
	<option value=\"\">Choose Taxonomy level...</option>";
	foreach ($arr as $value){
        	print "<option value='analyses/pie/$origin/$site_code/$value.html'>$value</option>\n";
		}
	print "<input type='button' value='go' onclick=\"window.open(setit.options[setit.selectedIndex].value)\">";
?>

<h2>Comparative analyses</h2>

<form name='form2' target="_blank" action='/cgi-bin/prompt/make-csv.cgi' method="GET">
	Choose Taxa Level:<br>

<?php
        foreach ($arr as $value){
		print "<input name=\"taxa\" type=\"radio\" value=\"$value\">$value\n";
                }
	print "<br>";

	echo "<p>";
	echo "Select sites:<br>";
	$MIC_opts = glob("analyses/abun/MIC/*");


	$col2 = 1;
	print "<b>MIC</b><br>\n";
       foreach ($MIC_opts as $heat_opt){
              $heat_opt = preg_replace("/analyses\/abun\/MIC\//i", '', $heat_opt);
              print "<input name='MIC_$heat_opt' type='checkbox' value='$heat_opt' >$heat_opt";
	      if ( is_int ($col2 / 10))
		print "<br>\n";
		$col2++;
	}
	$SEQ_opts = glob("analyses/abun/SEQ/*");
	$col2 = 1;
	print "<br><b>NGS</b><br>\n";
	foreach ($SEQ_opts as $heat_opt){
              $heat_opt = preg_replace("/analyses\/abun\/SEQ\//i", '', $heat_opt);
              print "<input name='SEQ_$heat_opt' type='checkbox' value='$heat_opt' >$heat_opt";
	      if ( is_int ($col2 / 10))
		print "<br>\n";
		$col2++;

        }
	echo "</p>";
	echo "<input type='submit' value='Collate Data' onclick=\"submit\">";
        echo "</form>";
	
	echo "<input type='button' value='Generate Heatmap' onclick=\"window.open('r_call.php'); window.open('tmp/current.pdf')\">";
	echo "<input type='button' value='Download data' onclick=\"window.open('tmp/compound_abun.csv')\">";
	echo "<br>n.b. If multiple pdf's are open, press refresh to view newest.<br>\n";
?>


</p>
</body>
</html>
