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
<img style="width: 700px; height: 150px;" alt="" src="images/prompt_logo.png" float:left="">&nbsp;
<hr>

<br><big style="font-weight: bold;">Choose a taxonomy level for pie chart fun!</font><br>

<?php
	$arr = array('phylum', 'class', 'order', 'family', 'genus', 'species');

	echo "<b>Data Origin:</b><br>\n";
	<input type="radio" name="origin" value="SEQ">Barcode Sequencing
	<input type="radio" name="origin" value="MIC">Microscopy

	echo "<form name='form1' action='./results.php'>";
	echo "<b>Select a Site:</b><br>\n";

	$sites = glob("DIATOMS_FULL/pie/*");


	foreach ($sites as $site){
		$site = preg_replace("/DIATOMS_FULL\/pie\//i", '', $site);

		#print "<input name=\"$site\" type=\"radio\" value=\"$site\" onclick=\"submit()\">$site<br>\n";
	
	}
	echo "</form>";
	
	foreach($_GET as $key=>$value){
		$$key = $value;
		$return = $value;
		print "<b>site: $return</b>";

	print "<br><select id='setit' name='url'>
	<option value=\"\">Choose Taxonomy level...</option>";
	foreach ($arr as $value){
        	print "<option value='DIATOMS_FULL/pie/$return/$value.html'>$value</option>\n";
		}
	print "<input type='button' value='go' onclick=\"window.open(setit.options[setit.selectedIndex].value)\">";

}
?>

<p><big style="font-weight: bold;">Select sites to be compared in a heat map:</big><br>

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
