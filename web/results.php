<html>
<head>
<title>php test page</title>
<style type="text/css">
body {background-image:url('images/diatom_back.jpg');}
</style>
</head>

<body>
<center>
<p>
<img style="width: 700px; height: 150px;" alt="" src="images/prompt_logo.png" float:left="">
</center>
<hr>

<h1>Taxonomic Analysis</h1>
<h2>Sample Pie charts</h2>

<form name='form1' action='./results.php'>
	<b>Data Origin:</b><br>
	<input type="radio" name="origin" value="SEQ" onclick=submit() selected >Barcode Sequencing
	<input type="radio" name="origin" value="MIC" onclick=submit() >Microscopy
</form>

<form name='form2' action='./results.php'>
<b>Select a Site:</b><br>
<?php
	foreach($_GET as $key=>$value){
        	$$key = $value;
                $origin = $value;
	}

	$sites = glob("analyses/$origin/*");

	foreach ($sites as $site){
		$site = preg_replace("/analyses\/$origin\//i", '', $site);
		print "<input name=\"site\" type=\"radio\" value=\"$site\"  onclick=\"submit()\">$site\n";
	
	}
?>
</form>

<?php	
	foreach($_GET as $key=>$value){
		$$key = $value;
		$site_code = $value;
		print "<b>site: $site_code</b>";
	


	$arr = array('phylum', 'class', 'order', 'family', 'genus', 'species');
	print "<br><select id='setit' name='url'>
	<option value=\"\">Choose Taxonomy level...</option>";
	foreach ($arr as $value){
        	print "<option value='analyses//$site_code/$value.html'>$value</option>\n";
		}
	print "<input type='button' value='go' onclick=\"window.open(setit.options[setit.selectedIndex].value)\">";

}
?>

<h2>Heatmap Comparison</h2>

<?php
	echo "<form name='form2' target=\"_blank\" action='/cgi-bin/metamod/make_csv.cgi'>";
	echo "Choose Taxa Level:<br>";

        foreach ($arr as $value){
		print "<input name=\"taxa\" type=\"radio\" value=\"$value\">$value\n";
                }
	print "<br>";

	echo "<p>";
	echo "Select sites:<br>";
	$heat_opts = glob("DIATOMS_FULL/abundance/*");

        foreach ($heat_opts as $heat_opt){
              $heat_opt = preg_replace("/DIATOMS_FULL\/abundance\//i", '', $heat_opt);
              print "<input name='$heat_opt' type='checkbox' value='$heat_opt' >$heat_opt<br>";

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
