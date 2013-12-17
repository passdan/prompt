<?php
	echo "Heatmap Generated<br>";
	echo system('/usr/bin/R < heatmap.R > NULL --vanilla');
?>	
